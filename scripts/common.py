"""
공통 모듈. config 로딩 · 홈택스 파일 파싱 · 상계 매칭 · 등급 판정.

중요: 임계값·색상·시트명은 전부 config/check-config.json 에서 읽는다.
이 파일에 숫자를 하드코딩하지 말 것. 하드코딩하는 순간 config 가 거짓말이 된다.
"""
import json
import os
import re
import glob
from datetime import date, timedelta

import pandas as pd

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- config

def load_config():
    with open(os.path.join(SKILL_DIR, "config", "check-config.json"), encoding="utf-8") as f:
        return json.load(f)


def load_vendors():
    with open(os.path.join(SKILL_DIR, "config", "vendors.json"), encoding="utf-8") as f:
        return json.load(f)["vendors"]


# ---------------------------------------------------------------- 사업자번호

def norm_biz(v):
    """하이픈·공백·전각문자 제거 후 숫자만. 전각 숫자도 반각으로 변환."""
    s = str(v)
    s = s.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    return re.sub(r"\D", "", s)


def fmt_biz(v):
    """표시용 하이픈 삽입. 저장은 항상 하이픈 없이."""
    s = norm_biz(v)
    return f"{s[:3]}-{s[3:5]}-{s[5:]}" if len(s) == 10 else s


def biz_checksum_ok(v):
    """국세청 사업자등록번호 체크섬. vendors.json 오타를 잡는다."""
    s = norm_biz(v)
    if len(s) != 10 or not s.isdigit():
        return False
    w = [1, 3, 7, 1, 3, 7, 1, 3, 5]
    d = [int(c) for c in s]
    total = sum(d[i] * w[i] for i in range(9)) + (d[8] * 5) // 10
    return (10 - total % 10) % 10 == d[9]


# ---------------------------------------------------------------- 기간·유예

def month_range(as_of):
    """점검 대상 월. 매년 1월 1일부터 실행월까지. range(1,10) 같은 고정값 금지."""
    return list(range(1, as_of.month + 1))


def deadline_for(year, month, deadline_day):
    """작성월 -> 발급기한(익월 deadline_day 일)."""
    y, m = (year + 1, 1) if month == 12 else (year, month + 1)
    return date(y, m, deadline_day)


def is_in_grace(year, month, as_of, cfg):
    """발급기한이 아직 안 지난 달인가. strict 모드면 항상 False."""
    g = cfg["grace"]
    if g["mode"] != "auto":
        return False
    return as_of <= deadline_for(year, month, g["deadline_day"])


def vat_period_of(month, cfg):
    if not cfg["vat_period"]["enabled"]:
        return ""
    for p in cfg["vat_period"]["periods"]:
        if month in p["months"]:
            return p["name"]
    return ""


# ---------------------------------------------------------------- 파일 로딩

def detect_kind(columns, cfg):
    """
    파일명이 아니라 컬럼 구성으로 판정한다.
    홈택스 다운로드 파일명이 바뀌어도, 사용자가 이름을 바꿔도 안전하다.
    """
    return "세" if cfg["input"]["tax_marker_column"] in columns else "계"


def load_uploads(upload_dir, cfg):
    """
    홈택스 .xls 를 전부 읽어 하나로 합친다.
    반환: (df, meta) — meta 에는 파일별 헤더 총계·기간이 담긴다(대사 검증용).
    """
    files = sorted(glob.glob(os.path.join(upload_dir, "*.xls"))) + \
        sorted(glob.glob(os.path.join(upload_dir, "*.xlsx")))
    if not files:
        raise SystemExit(f"[중단] {upload_dir} 에 홈택스 파일(.xls)이 없습니다.")

    hdr = cfg["input"]["header_row"]
    frames, meta = [], []
    for f in files:
        base = os.path.basename(f)
        # 헤더 영역(총 공급가액 등)을 먼저 읽어 대사용으로 보관
        head = pd.read_excel(f, header=None, nrows=hdr, dtype=str)
        declared = _declared_total(head)

        d = pd.read_excel(f, header=hdr, dtype=str)
        missing = [c for c in cfg["input"]["required_columns"] if c not in d.columns]
        if missing:
            raise SystemExit(f"[중단] {base}: 필수 컬럼 없음 {missing}. 홈택스 양식이 바뀌었을 수 있습니다.")

        d = d.dropna(subset=["작성일자"]).copy()
        d["구분"] = detect_kind(d.columns, cfg)
        d["원본파일"] = base
        # 중복 컬럼(상호/주소 등)은 pandas 가 .1 접미사를 붙인다.
        # 위치 인덱스로 참조하면 홈택스가 컬럼 하나만 추가해도 깨지므로 명시적으로 이름을 준다.
        d["공급받는자상호"] = _receiver_name(d)
        frames.append(d)
        meta.append({
            "file": base, "kind": d["구분"].iloc[0] if len(d) else "?",
            "rows": len(d), "declared_total": declared,
        })

    df = pd.concat(frames, ignore_index=True)
    df["공급가액n"] = _num(df["공급가액"])
    df["합계금액n"] = _num(df["합계금액"])
    df["공급자번호"] = df["공급자사업자등록번호"].map(norm_biz)
    df["받는자번호"] = df["공급받는자사업자등록번호"].map(norm_biz)
    df["작성일"] = pd.to_datetime(df["작성일자"])
    df["월"] = df["작성일"].dt.month
    df["연"] = df["작성일"].dt.year
    df = df.sort_values(["작성일", "공급자번호"]).reset_index(drop=True)
    return df, meta


def _num(s):
    return pd.to_numeric(
        s.astype(str).str.replace(",", "").str.strip(), errors="coerce"
    ).fillna(0)


def _receiver_name(d):
    """공급받는자사업자등록번호 바로 다음다음 열이 공급받는자 상호."""
    cols = list(d.columns)
    i = cols.index("공급받는자사업자등록번호")
    for c in cols[i + 1:i + 4]:
        if str(c).startswith("상호"):
            return d[c]
    return pd.Series([""] * len(d), index=d.index)


def _declared_total(head):
    """헤더 영역의 '총 공급가액' 값을 뽑는다. 없으면 None."""
    # pd.NA 가 섞이므로 astype(str) 만으로는 부족하다. 원소 단위로 강제 변환한다.
    flat = [str(x) for x in head.values.flatten().tolist()]
    for i, v in enumerate(flat):
        if "총" in v and "공급가액" in v and i + 1 < len(flat):
            try:
                return int(str(flat[i + 1]).replace(",", ""))
            except ValueError:
                return None
    return None


# ---------------------------------------------------------------- 상계 매칭

def match_offsets(df, cfg):
    """
    마이너스 건을 원본과 짝짓는다.

    금액 절대값만 보고 짝지으면, 매월 같은 금액이 나오는 거래처(예: 통신비 21,000원)
    에서 엉뚱한 달과 붙는다. 그래서 품목명까지 함께 본다.
    짝을 못 찾은 마이너스는 취소가 아니라 환급·할인성으로 보고 순액에만 반영한다.
    """
    df["상계"] = ""
    o = cfg["offset_matching"]
    pairs = 0

    for _, g in df.groupby("공급자번호"):
        used = set()
        for i, r in g[g["공급가액n"] < 0].sort_values("작성일").iterrows():
            same_amt = g[(g["공급가액n"] == -r["공급가액n"]) & (~g.index.isin(used))]
            same_amt = same_amt[same_amt.index != i]
            item = str(r.get("품목명", ""))
            same_item = same_amt[same_amt["품목명"].astype(str) == item]

            buckets = {
                "same_date_same_item": same_item[same_item["작성일"] == r["작성일"]],
                "same_month_same_item": same_item[same_item["월"] == r["월"]],
                "same_date": same_amt[same_amt["작성일"] == r["작성일"]],
                "same_month": same_amt[same_amt["월"] == r["월"]],
                "any_earlier": same_amt[same_amt["작성일"] <= r["작성일"]],
            }
            order = list(o["priority"])
            if o["require_same_item_name"]:
                order = [k for k in order if "same_item" in k] + \
                    [k for k in order if "same_item" not in k and k == "any_earlier"]

            for key in order:
                cand = buckets.get(key)
                if cand is not None and len(cand):
                    j = cand.index[0]
                    used.update({i, j})
                    df.loc[i, "상계"] = "취소분(상계)"
                    df.loc[j, "상계"] = "원본(상계됨)"
                    pairs += 1
                    break
            else:
                df.loc[i, "상계"] = "환급·할인(순액반영)"
    return pairs


def live_rows(g):
    """상계로 소멸되지 않은 유효 건. 빈 DataFrame 에서도 안전하다."""
    if len(g) == 0:
        return g
    return g[~g["상계"].astype(str).str.contains("상계", na=False)]
