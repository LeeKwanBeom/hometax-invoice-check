"""
공통 모듈. config 로딩 · 홈택스 파일 파싱 · 점검 기간 · 상계 매칭.

중요: 임계값·색상·시트명은 전부 config/check-config.json 에서 읽는다.
이 파일에 숫자를 하드코딩하지 말 것. 하드코딩하는 순간 config 가 거짓말이 된다.
validate.py 의 '임계값 단일 출처' 검사가 이걸 실제로 감시한다.
"""
import json
import os
import re
import glob
from datetime import date, timedelta

import pandas as pd

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- config

def _load_json(path, what, hint):
    """JSON 로딩 실패를 트레이스백 대신 사람이 읽는 메시지로 바꾼다."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"[중단] {what} 파일이 없습니다: {path}\n       {hint}")
    except json.JSONDecodeError as e:
        raise SystemExit(
            f"[중단] {what} 파일이 깨졌습니다: {path}\n"
            f"       {e.lineno}행 {e.colno}열 — {e.msg}\n       {hint}"
        )


def load_config():
    return _load_json(os.path.join(SKILL_DIR, "config", "check-config.json"),
                      "설정(check-config.json)",
                      "sync.py 로 저장소 최신본을 다시 받으세요.")


def load_vendors():
    d = _load_json(os.path.join(SKILL_DIR, "config", "vendors.json"),
                   "거래처 목록(vendors.json)",
                   "sync.py 로 저장소 최신본을 다시 받으세요.")
    if "vendors" not in d:
        raise SystemExit("[중단] vendors.json 에 'vendors' 키가 없습니다.")
    return d["vendors"]


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


# ---------------------------------------------------------------- 점검 기간

def month_range(as_of):
    """
    점검 대상 (연, 월) 목록. 당해 1월부터 실행월까지.

    **1월에 실행할 때는 전년 12월을 앞에 붙인다.** 12월분 발급기한은 익년 1/10 이라
    12월에 돌리면 항상 유예이고, 1월이 되면 연도가 바뀌어 사라진다. 붙이지 않으면
    12월분은 영영 판정되지 않고, 2기 확정신고(1/25) 직전 점검에서 가장 중요한 달이
    통째로 빠진다.

    range(1, 10) 같은 고정값 금지.
    """
    months = [(as_of.year, m) for m in range(1, as_of.month + 1)]
    if as_of.month == 1:
        months.insert(0, (as_of.year - 1, 12))
    return months


def month_label(ym, as_of):
    """매트릭스 열 머리말. 전년도 달은 구분해서 보여준다."""
    y, m = ym
    return f"{m}월" if y == as_of.year else f"전년 {m}월"


def clip_period(df, months, as_of=None):
    """
    점검 대상 (연,월) 밖의 행과 기준일 이후의 행을 잘라낸다.

    리포트·검증이 **같은 규칙**을 쓰도록 한 곳에 모아둔다. 서로 다르게 자르면
    멀쩡한 산출물에 FAIL 이 난다(원본정제데이터는 안 자르고 검증만 자르던 버그).

    as_of 절단이 없으면 `--as-of` 로 과거 시점을 재현할 수 없다. 이후 데이터가
    섞여 최종수취일이 미래가 되고, 경과일이 음수가 되어 판정이 통째로 사라진다.
    """
    if len(df) == 0:
        return df
    keys = set(months)
    mask = pd.Series([(y, m) in keys for y, m in zip(df["연"], df["월"])],
                     index=df.index)
    if as_of is not None:
        mask &= (df["작성일"].dt.date <= as_of)
    return df[mask]


def deadline_for(year, month, deadline_day):
    """작성월 -> 발급기한(익월 deadline_day 일)."""
    y, m = (year + 1, 1) if month == 12 else (year, month + 1)
    return date(y, m, deadline_day)


def is_in_grace(year, month, as_of, cfg):
    """
    발급기한이 아직 안 지난 달인가.

    실행 당월은 **모드와 무관하게** 유예다. 아직 끝나지 않은 달이라
    미수취로 확정할 근거 자체가 없다. strict 를 '유예 없음'으로 곧이곧대로
    구현하면 당월이 전 거래처 결번이 되어(9/6 실행시 확인 필요 6건 → 26건)
    정작 쓰라고 만든 신고 직전 점검에서 못 쓰게 된다.

    그 외의 달은 strict 면 유예 없음, auto 면 익월 deadline_day 까지 유예.
    """
    if year == as_of.year and month == as_of.month:
        return True
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


def _read_excel(path, **kw):
    try:
        return pd.read_excel(path, **kw)
    except ImportError:
        raise SystemExit(
            "[중단] 홈택스 .xls 를 읽으려면 xlrd 가 필요합니다.\n"
            "       pip install xlrd --break-system-packages"
        )


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
        head = _read_excel(f, header=None, nrows=hdr, dtype=str)
        declared = _declared_total(head)

        d = _read_excel(f, header=hdr, dtype=str)
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
            same_item = same_amt[same_amt["품목명"].astype(str) == item] \
                if "품목명" in same_amt.columns else same_amt.iloc[0:0]

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
