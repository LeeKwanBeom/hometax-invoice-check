"""
산출물 xlsx 자체 검증. build_report.py 직후에 반드시 돌린다.

설계 원칙: **0건 매칭이면 PASS 가 아니라 FAIL 이다.**
"미수취 칸에 색이 칠해져 있지 않다"는, 정말 없어서일 수도 있지만
셀을 못 찾아서일 수도 있다. 후자를 PASS 로 넘기면 검증이 무의미해진다.
그래서 모든 검사는 '검사 대상을 몇 개 찾았는지'를 먼저 보고한다.

열은 반드시 헤더 '이름'으로 찾는다. 인덱스 하드코딩 금지 —
열이 하나만 추가돼도 엉뚱한 칸을 검사하게 된다.

사용법:
    python scripts/validate.py <출력.xlsx> [--uploads DIR] [--as-of YYYY-MM-DD] [--strict]

build_report.py 에 준 `--as-of` / `--strict` 는 **여기에도 똑같이 준다.**
안 주면 검증기가 다른 기준으로 판단해서 멀쩡한 산출물에 FAIL 을 낸다.
"""
import argparse
import json
import os
import re
import sys
from datetime import date

import pandas as pd
from openpyxl import load_workbook

from common import (SKILL_DIR, load_config, load_vendors, load_uploads,
                    match_offsets, drop_split_offsets, norm_biz, month_range,
                    month_label, clip_period, is_in_grace, is_resolved)

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"
_res = []


def rec(level, name, detail=""):
    _res.append((level, name, detail))


def hdr_map(ws, row):
    """헤더 행에서 {이름: 열번호}. 위치 대신 이름으로 찾기 위한 것."""
    return {str(c.value).strip(): c.column for c in ws[row] if c.value}


def find_header_row(ws, must_have, limit=8):
    for r in range(1, min(limit, ws.max_row) + 1):
        m = hdr_map(ws, r)
        if all(k in m for k in must_have):
            return r, m
    return None, {}


def col_values(ws, r, col):
    """헤더 아래 데이터 행의 (행번호, 값) 목록."""
    return [(i, ws.cell(i, col).value) for i in range(r + 1, ws.max_row + 1)]


# ---------------------------------------------------------------- 검사

def check_sheets(wb, cfg):
    # config 의 _comment 키는 설정값이 아니다.
    want = [v for k, v in cfg["sheets"].items() if not k.startswith("_")]
    missing = [s for s in want if s not in wb.sheetnames]
    if missing:
        rec(FAIL, "시트 구성", f"없는 시트: {missing} / 실제: {wb.sheetnames}")
    else:
        rec(PASS, "시트 구성", " · ".join(wb.sheetnames))


def check_matrix_months(wb, cfg, as_of):
    ws = wb[cfg["sheets"]["matrix"]]
    want = [month_label(ym, as_of) for ym in month_range(as_of)]
    r, m = find_header_row(ws, ["공급자번호", "상호"])
    if not r:
        rec(FAIL, "매트릭스 헤더", "'공급자번호'/'상호' 헤더 행을 못 찾음")
        return None, None
    found = [k for k in m if k.endswith("월")]
    if found != want:
        rec(FAIL, "매트릭스 월 컬럼",
            f"기대 {want}\n실제 {found}\n월 범위가 고정값으로 박혀 있을 수 있다.")
    else:
        rec(PASS, "매트릭스 월 컬럼", f"{want[0]}~{want[-1]} · {len(want)}개")
    return r, m


def check_matrix_blank_and_fill(wb, cfg, as_of):
    """
    미수취 = 값 없음 + 채우기 없음.
    전액취소 = 값 0 + 노랑.
    검사 대상을 하나도 못 찾으면 FAIL (마크업이 바뀐 것).
    """
    ws = wb[cfg["sheets"]["matrix"]]
    r, m = find_header_row(ws, ["공급자번호", "상호"])
    if not r:
        return
    mcols = [m[month_label(ym, as_of)] for ym in month_range(as_of)
             if month_label(ym, as_of) in m]
    if not mcols:
        rec(FAIL, "매트릭스 셀 검사", "월 컬럼을 하나도 못 찾음 — 이후 검사 무의미")
        return

    blank, cancelled, bad_blank, bad_zero = 0, 0, [], []
    yellow = (cfg["colors"]["cancelled"] or "").upper()
    for row in ws.iter_rows(min_row=r + 1, max_row=ws.max_row):
        for ci in mcols:
            c = ws.cell(row[0].row, ci)
            fill = (c.fill.fgColor.rgb or "") if c.fill and c.fill.fill_type else ""
            fill = str(fill).upper()[-6:]
            if c.value is None:
                blank += 1
                if fill == yellow:
                    bad_blank.append(c.coordinate)
            elif c.value == 0:
                cancelled += 1
                if fill != yellow:
                    bad_zero.append(c.coordinate)

    if blank == 0:
        rec(FAIL, "미수취=공란 검사", "공란 셀을 하나도 못 찾음. 셀 값 표기 방식이 바뀌었을 수 있다.")
    elif bad_blank:
        rec(FAIL, "미수취=공란 검사", f"공란인데 취소색이 칠해진 셀: {bad_blank[:10]}")
    else:
        rec(PASS, "미수취=공란 검사", f"공란 {blank}칸 확인 · 잘못된 채우기 없음")

    if cancelled == 0:
        rec(SKIP, "전액취소=0+노랑 검사", "값 0 인 셀이 없음 (이번 데이터에 전액취소 없음)")
    elif bad_zero:
        rec(FAIL, "전액취소=0+노랑 검사", f"0 인데 노랑이 아닌 셀: {bad_zero[:10]}")
    else:
        rec(PASS, "전액취소=0+노랑 검사", f"{cancelled}칸 전부 노랑")


def check_vendor_coverage(wb, cfg, vendors):
    """vendors.json 의 모든 거래처가 매트릭스에 행으로 존재해야 한다."""
    ws = wb[cfg["sheets"]["matrix"]]
    r, m = find_header_row(ws, ["공급자번호", "상호"])
    if not r:
        return
    col = m["공급자번호"]
    seen = {norm_biz(ws.cell(i, col).value)
            for i in range(r + 1, ws.max_row + 1) if ws.cell(i, col).value}
    want = {norm_biz(v["biz_no"]) for v in vendors}
    miss = want - seen
    if not vendors:
        rec(SKIP, "점검 대상 누락 검사", "vendors.json 이 비어 있음")
    elif miss:
        rec(FAIL, "점검 대상 누락 검사",
            f"매트릭스에 행이 없는 거래처 {len(miss)}곳: {sorted(miss)[:10]}\n"
            "데이터를 groupby 해서 만들면 '0건 거래처'가 사라진다.")
    else:
        rec(PASS, "점검 대상 누락 검사", f"{len(want)}곳 전부 행 존재")


def check_totals(wb, cfg, df):
    """매트릭스 월별 합 == 원본정제데이터 합. 집계 버그를 잡는다."""
    ws = wb[cfg["sheets"]["matrix"]]
    r, m = find_header_row(ws, ["공급자번호", "상호"])
    if not r or "순공급가액" not in m:
        rec(FAIL, "합계 대사", "'순공급가액' 열을 못 찾음")
        return
    col = m["순공급가액"]
    total = sum(ws.cell(i, col).value or 0 for i in range(r + 1, ws.max_row + 1))
    raw = int(df["공급가액n"].sum())
    if total != raw:
        rec(FAIL, "합계 대사", f"매트릭스 {total:,} vs 원본 {raw:,} · 차 {total-raw:,}")
    else:
        rec(PASS, "합계 대사", f"{total:,}원 일치")


def check_raw_rows(wb, cfg, df):
    ws = wb[cfg["sheets"]["raw"]]
    got = ws.max_row - 1
    if got != len(df):
        rec(FAIL, "원본 행수", f"시트 {got}행 vs 데이터 {len(df)}건")
    else:
        rec(PASS, "원본 행수", f"{got}건")


def check_no_duplicates(wb, cfg):
    """
    원본정제데이터의 승인번호 중복. 같은 구간 파일을 두 번 올린 경우를 잡는다.

    check_input.py 에도 같은 검사가 있지만, 그 단계를 건너뛰면 리포트가
    오류 없이 만들어지고 금액이 부풀려진 채 그대로 나간다(441건 → 521건,
    상계쌍 6 → 8쌍). 산출물만 보고도 잡히도록 여기서 한 번 더 본다.
    원본 행수 검사는 산출물을 자기 입력과 비교하므로 이 경우를 못 잡는다.
    """
    ws = wb[cfg["sheets"]["raw"]]
    r, m = find_header_row(ws, ["승인번호"])
    if not r:
        rec(FAIL, "승인번호 중복", "'승인번호' 열을 못 찾음 — 중복 검사를 못 했다")
        return
    col = m["승인번호"]
    seen, dup = set(), []
    for i in range(r + 1, ws.max_row + 1):
        v = ws.cell(i, col).value
        if v is None or str(v).strip() == "":
            continue
        v = str(v).strip()
        if v in seen:
            dup.append(v)
        seen.add(v)
    if not seen:
        rec(FAIL, "승인번호 중복", "승인번호가 한 건도 없음 — 검사 대상을 못 찾았다")
    elif dup:
        rec(FAIL, f"승인번호 중복 {len(dup)}건",
            "같은 구간 홈택스 파일을 두 번 올렸을 가능성이 높다.\n"
            "그대로 두면 금액과 상계쌍이 부풀려진다. 중복분을 빼고 다시 만들 것.\n" +
            "\n".join(dup[:10]))
    else:
        rec(PASS, "승인번호 중복", f"{len(seen)}건 전부 고유")


def check_monthly_totals(wb, cfg, as_of):
    """
    매트릭스 **월별** 합 == 원본정제데이터 월별 합.

    지금까지는 '순공급가액' 총합만 대사했다. 총합이 맞아도 월이 한 칸씩
    밀려 있으면 그대로 통과한다. 월 컬럼 자체가 이 리포트의 본체다.
    """
    mx = wb[cfg["sheets"]["matrix"]]
    rw = wb[cfg["sheets"]["raw"]]
    r, m = find_header_row(mx, ["공급자번호", "상호"])
    rr, rm = find_header_row(rw, ["작성일자", "공급가액"])
    if not r or not rr:
        rec(FAIL, "월별 합 대사", "매트릭스 또는 원본정제데이터 헤더를 못 찾음")
        return

    raw_sum = {}
    for i in range(rr + 1, rw.max_row + 1):
        d = rw.cell(i, rm["작성일자"]).value
        v = rw.cell(i, rm["공급가액"]).value
        if d is None:
            continue
        ts = pd.to_datetime(str(d), errors="coerce")
        if pd.isna(ts):
            continue
        raw_sum[(ts.year, ts.month)] = raw_sum.get((ts.year, ts.month), 0) + (v or 0)

    if not raw_sum:
        rec(FAIL, "월별 합 대사", "원본정제데이터에서 작성일자를 하나도 못 읽음")
        return

    diffs, checked = [], 0
    for ym in month_range(as_of):
        label = month_label(ym, as_of)
        if label not in m:
            continue
        checked += 1
        col = sum(v or 0 for _, v in col_values(mx, r, m[label]))
        if col != raw_sum.get(ym, 0):
            diffs.append(f"{label}: 매트릭스 {col:,} vs 원본 {raw_sum.get(ym, 0):,}")
    if checked == 0:
        rec(FAIL, "월별 합 대사", "대사할 월 컬럼을 하나도 못 찾음")
    elif diffs:
        rec(FAIL, f"월별 합 대사 불일치 {len(diffs)}개월", "\n".join(diffs))
    else:
        rec(PASS, "월별 합 대사", f"{checked}개월 전부 일치")


def check_offsets(wb, cfg):
    """
    상계 매칭 결과의 타당성. 지금까지 아무 검사도 없던 구간이다.

    '취소분(상계)' 과 '원본(상계됨)' 은 짝이므로 개수가 같아야 한다.
    마이너스 건이 있는데 쌍이 0개면 매칭이 통째로 안 돈 것이다.
    """
    ws = wb[cfg["sheets"]["raw"]]
    r, m = find_header_row(ws, ["상계처리", "공급가액"])
    if not r:
        rec(FAIL, "상계 매칭", "'상계처리' 열을 못 찾음")
        return
    cancel = orig = refund = neg = split = 0
    for i in range(r + 1, ws.max_row + 1):
        v = str(ws.cell(i, m["상계처리"]).value or "")
        amt = ws.cell(i, m["공급가액"]).value or 0
        if amt < 0:
            neg += 1
        if v.startswith("취소분"):
            cancel += 1
        elif v.startswith("원본"):
            orig += 1
        elif "순액반영" in v:
            refund += 1
        elif v.startswith("짝이 기간 밖"):
            # 짝을 기간 밖에서 맺은 건. 개수가 안 맞는 게 정상이고,
            # build_report 가 상계 표시를 이미 해제했으므로 죽은 건이 아니다.
            split += 1
    if cancel != orig:
        rec(FAIL, "상계 매칭", f"취소분 {cancel}건 vs 원본 {orig}건 — 짝이 안 맞는다")
    elif neg and cancel == 0 and refund == 0:
        rec(FAIL, "상계 매칭",
            f"마이너스 {neg}건이 있는데 상계도 환급도 0건 — 매칭이 안 돌았다")
    elif neg == 0:
        rec(SKIP, "상계 매칭", "마이너스 건이 없음")
    else:
        rec(PASS, "상계 매칭", f"{cancel}쌍 · 환급·할인 {refund}건 · 마이너스 {neg}건"
            + (f" · 짝이 기간 밖 {split}건" if split else ""))


def check_unlisted(wb, cfg, vendors):
    """대상외공급자 시트. 지금까지 검사가 하나도 없던 시트다."""
    ws = wb[cfg["sheets"]["unlisted"]]
    mx = wb[cfg["sheets"]["matrix"]]
    r, m = find_header_row(ws, ["공급자번호", "추가 권장"])
    if not r:
        rec(FAIL, "대상외공급자 시트", "'공급자번호'/'추가 권장' 헤더를 못 찾음")
        return
    seen = {norm_biz(v) for _, v in col_values(ws, r, m["공급자번호"]) if v}
    listed = {norm_biz(v["biz_no"]) for v in vendors}

    overlap = seen & listed
    if overlap:
        rec(FAIL, "대상외공급자 시트",
            f"vendors.json 에 있는데 '대상외'로 분류된 곳 {len(overlap)}: {sorted(overlap)[:5]}")
        return

    mr, mm = find_header_row(mx, ["공급자번호", "대상"])
    if mr:
        want = {norm_biz(mx.cell(i, mm["공급자번호"]).value)
                for i in range(mr + 1, mx.max_row + 1)
                if str(mx.cell(i, mm["대상"]).value) == "대상외"}
        if want != seen:
            rec(FAIL, "대상외공급자 시트",
                f"매트릭스의 '대상외' {len(want)}곳과 시트 {len(seen)}곳이 다름")
            return
    if not seen:
        rec(SKIP, "대상외공급자 시트", "대상외 공급자가 없음")
    else:
        n_rec = sum(1 for _, v in col_values(ws, r, m["추가 권장"]) if v)
        rec(PASS, "대상외공급자 시트", f"{len(seen)}곳 · 추가 권장 {n_rec}곳")


def check_grades(wb, cfg, vendors):
    """
    미수취목록의 등급 분류가 형태적으로 옳은지. 지금까지 '기한 전' 건수만 셌다.

      - 등급값이 정해진 집합 안에 있는가
      - 정렬이 등급 순인가(조치 대상이 위로 오는가)
      - vendors.json 에 없는 공급자가 조치 목록에 섞이지 않았는가
      - '확인 필요'로 지목한 결번 월이 매트릭스에서 실제로 공란인가
    """
    ws = wb[cfg["sheets"]["missing"]]
    mx = wb[cfg["sheets"]["matrix"]]
    r, m = find_header_row(ws, ["등급", "공급자번호", "누락된 월"])
    if not r:
        rec(FAIL, "등급 분류", "미수취목록 헤더를 못 찾음")
        return
    order = {"확인 필요": 0, "기한 전": 1, "단발·비정기": 2, "정상": 3,
             "거래 종료": 4, "해결": 5}
    listed = {norm_biz(v["biz_no"]) for v in vendors}
    mr, mm = find_header_row(mx, ["공급자번호", "상호"])
    mrow = {norm_biz(mx.cell(i, mm["공급자번호"]).value): i
            for i in range(mr + 1, mx.max_row + 1)} if mr else {}

    bad, prev, n = [], -1, 0
    for i in range(r + 1, ws.max_row + 1):
        g = ws.cell(i, m["등급"]).value
        if g is None:
            continue
        n += 1
        g = str(g).strip()
        if g not in order:
            bad.append(f"{i}행: 알 수 없는 등급 '{g}'")
            continue
        if order[g] < prev:
            bad.append(f"{i}행: 등급 정렬이 뒤집힘 ('{g}' 가 뒤에)")
        prev = max(prev, order[g])
        sid = norm_biz(ws.cell(i, m["공급자번호"]).value)
        if sid not in listed:
            bad.append(f"{i}행: vendors.json 에 없는 공급자 {sid}")
        if g == "확인 필요" and mrow.get(sid):
            for label in str(ws.cell(i, m["누락된 월"]).value or "").split(", "):
                label = label.strip()
                if label and label in mm:
                    v = mx.cell(mrow[sid], mm[label]).value
                    if v not in (None, 0):
                        bad.append(f"{i}행: 결번으로 적힌 {label} 에 매트릭스 값 {v}")
    if n == 0 and mrow:
        # 아무도 안 잡힌 실행에서 미수취목록 0행은 정상이다(1월 초가 대표적).
        # 이걸 FAIL 로 내면 tests 의 '1월 초 실행이 전 거래처를 확인 필요로
        # 만들지 않음' 과 정면으로 충돌한다. 헤더를 찾았고 매트릭스에 점검대상
        # 행이 있으면 마크업이 바뀐 게 아니므로 SKIP 이 맞다.
        rec(SKIP, "등급 분류", "미수취목록이 비어 있음 — 이번 회차에 잡힌 거래처가 없다")
    elif n == 0:
        rec(FAIL, "등급 분류",
            "미수취목록도 매트릭스도 비어 있음 — 검사 대상을 못 찾았다")
    elif bad:
        rec(FAIL, f"등급 분류 이상 {len(bad)}건", "\n".join(bad[:10]))
    else:
        rec(PASS, "등급 분류", f"{n}행 · 등급값·정렬·결번 표기 정상")


def check_state(wb, cfg):
    """
    상태 열(신규/계속/해결)이 state/last-run.json 과 맞는지.

    '해결'은 한 번만 표시되고 사라져야 하므로 이력에 남아 있으면 안 된다.
    """
    ws = wb[cfg["sheets"]["missing"]]
    r, m = find_header_row(ws, ["등급"])
    if not r or "상태" not in m:
        rec(SKIP, "실행 이력 비교", "상태 열이 없음(--no-state 로 만든 산출물)")
        return
    p = os.path.join(SKILL_DIR, cfg["state"]["path"])
    if not os.path.exists(p):
        rec(FAIL, "실행 이력 비교", f"상태 열은 있는데 이력 파일이 없다: {p}")
        return
    try:
        saved = {x["biz_no"] for x in json.load(open(p, encoding="utf-8"))["flagged"]}
    except Exception as e:
        rec(FAIL, "실행 이력 비교", f"이력 파일을 읽을 수 없다: {e}")
        return
    action, resolved = set(), set()
    for i in range(r + 1, ws.max_row + 1):
        g = str(ws.cell(i, m["등급"]).value or "").strip()
        s = str(ws.cell(i, m["상태"]).value or "").strip()
        sid = norm_biz(ws.cell(i, m["공급자번호"]).value)
        if g == "확인 필요":
            action.add(sid)
        # 등급만 보면 '거래 종료 + 상태=해결' 행이 통째로 빠진다.
        elif is_resolved(g, s):
            resolved.add(sid)
    if action != saved:
        rec(FAIL, "실행 이력 비교",
            f"확인 필요 {len(action)}곳과 이력 {len(saved)}곳이 다름\n"
            f"리포트에만: {sorted(action - saved)[:5]} / 이력에만: {sorted(saved - action)[:5]}")
    elif resolved & saved:
        rec(FAIL, "실행 이력 비교",
            f"'해결'인데 이력에 남아 있음 — 다음 실행에도 또 뜬다: {sorted(resolved & saved)}")
    else:
        rec(PASS, "실행 이력 비교", f"확인 필요 {len(action)}곳 저장 · 해결 {len(resolved)}곳")


def check_resolved(wb, cfg):
    """
    '해결' 집계가 **등급 열과 상태 열을 모두** 세는지.

    이 검사가 없던 동안 build_report 콘솔과 validate 가 나란히 '해결 0' 을
    찍었고, 시트에는 `상태=해결` 행이 2개 있었다. 둘 다 등급 열만 셌기 때문이다.
    산출물은 옳고 요약만 틀리는 형태라 다른 검사로는 영영 안 걸린다.

    두 경로가 표기를 다르게 남긴다.
      - 새 행 경로  : 등급 '해결' + 상태 '해결' 을 **함께** 붙인다
      - 상태만 경로 : 기존 행의 등급은 그대로 두고 상태만 '해결' 로 바꾼다
    그래서 `상태열만` 이 0 이 아니면, 등급만 세는 코드는 그만큼 적게 센다.
    콘솔의 '해결 N' 과 여기 '총 N건' 이 다르면 한쪽이 다시 한 표기만 세는 것이다.
    """
    ws = wb[cfg["sheets"]["missing"]]
    r, m = find_header_row(ws, ["등급"])
    if not r:
        rec(FAIL, "해결 집계", "'등급' 열을 못 찾음")
        return
    if "상태" not in m:
        rec(SKIP, "해결 집계", "상태 열이 없음(--no-state 로 만든 산출물)")
        return

    by_grade, total, rows, bad = 0, 0, 0, []
    for i in range(r + 1, ws.max_row + 1):
        g = str(ws.cell(i, m["등급"]).value or "").strip()
        if not g:
            continue
        rows += 1
        s = str(ws.cell(i, m["상태"]).value or "").strip()
        if g == "해결":
            by_grade += 1
            if s != "해결":
                bad.append(f"{i}행")
        if is_resolved(g, s):
            total += 1

    if rows == 0:
        rec(SKIP, "해결 집계", "미수취목록이 비어 있음")
    elif total == 0:
        rec(SKIP, "해결 집계", "이번 회차에 해결된 거래처가 없음")
    elif bad:
        # 새 행 경로는 등급·상태를 **함께** 붙인다(apply_state). 등급만 '해결'
        # 인 행이 있으면 상태 부여가 빠진 것이고, 상태 열로 세는 쪽이 어긋난다.
        rec(FAIL, "해결 집계",
            f"등급은 '해결' 인데 상태가 비어 있는 행 {len(bad)}개: {bad[:10]}")
    else:
        rec(PASS, "해결 집계",
            f"총 {total}건 (등급열 {by_grade} · 상태열만 {total - by_grade}) — "
            f"콘솔의 '해결' 숫자와 같아야 한다")


def check_grace(wb, cfg, as_of):
    """유예 판정이 실제로 작동했는지. auto 모드인데 유예 칸이 0이면 의심."""
    if cfg["grace"]["mode"] != "auto":
        rec(SKIP, "발급기한 유예", "strict 모드")
        return
    ws = wb[cfg["sheets"]["missing"]]
    r, m = find_header_row(ws, ["등급"])
    if not r:
        rec(FAIL, "발급기한 유예", "'등급' 열을 못 찾음")
        return
    col = m["등급"]
    n = sum(1 for i in range(r + 1, ws.max_row + 1)
            if str(ws.cell(i, col).value) == "기한 전")
    prev = as_of.month - 1
    expect = prev >= 1 and is_in_grace(as_of.year, prev, as_of, cfg)
    if expect and n == 0:
        rec(FAIL, "발급기한 유예",
            f"{prev}월분 기한({cfg['grace']['deadline_day']}일)이 안 지났는데 '기한 전' 판정이 0건. "
            "유예 로직이 안 걸렸을 수 있다.")
    else:
        rec(PASS, "발급기한 유예", f"'기한 전' {n}건 (전월 유예 구간: {expect})")


def check_paths(cfg):
    """
    저장소에서 받아온 파일이 실제로 다 있는지.
    SKILL.md 도 이제 저장소에 있으므로(push --code 대상) 함께 본다.
    """
    want = ["SKILL.md", "README.md", "sync.py",
            "config/check-config.json", "config/vendors.json",
            "references/column-mapping.md", "references/judgment-rules.md",
            "references/excel-format.md", "scripts/common.py",
            "scripts/check_input.py", "scripts/build_report.py",
            "scripts/validate.py", "scripts/push.py",
            "tests/test_edge_cases.py"]
    miss = [p for p in want if not os.path.exists(os.path.join(SKILL_DIR, p))]
    if miss:
        rec(FAIL, "경로 존재 확인",
            f"없는 파일: {miss}\nsync.py 를 다시 돌려 저장소에서 받으세요.")
    else:
        rec(PASS, "경로 존재 확인", f"{len(want)}개 전부 존재")


def check_config_single_source(cfg):
    """
    config 가 거짓말을 시작하는 두 방향을 모두 본다.

      (a) 죽은 키   — config 에 있는데 코드가 한 번도 안 읽는 값.
                      바꿔도 아무 일이 안 일어나므로 읽는 사람을 속인다.
      (b) 하드코딩  — config 값이 코드·문서에 리터럴로 다시 적힌 곳.

    이전 버전은 thresholds 3개를 4가지 패턴으로만 훑어서, 정작 가장 경계하던
    `range(1, 10)` 월 고정값을 원리적으로 못 잡았다(10 이 임계값에 없으므로).
    0건 매칭이 곧 PASS 였던 셈이다.
    """
    # 주석·독스트링은 떼고 본다. 설명문에 적힌 예시("range(1, 10) 같은 고정값 금지")
    # 까지 위반으로 세면 검사가 시끄러워져서 아무도 안 보게 된다.
    tq = ['"' * 3, "'" * 3]

    def code_only(src):
        for q in tq:
            src = re.sub(q + r"[\s\S]*?" + q, "", src)
        return re.sub(r"#.*", "", src)

    py = {}
    for fn in os.listdir(os.path.join(SKILL_DIR, "scripts")):
        if fn.endswith(".py"):
            py[f"scripts/{fn}"] = code_only(open(
                os.path.join(SKILL_DIR, "scripts", fn), encoding="utf-8").read())
    # 문서 스캔 범위. references/ 만 보던 동안 SKILL.md 의 deadline_day 사본이
    # 1곳 → 3곳으로 늘어나도 FAIL 0 이 나왔다. 설명서·README·부트스트랩까지 본다.
    #
    # audit/ 는 **일부러 뺀다.** 점검 기준선은 문제가 된 원문을 그대로 인용해
    # 보관하는 파일이라, 여기를 스캔하면 인용문이 전부 위반으로 잡혀
    # 검사가 시끄러워지고 아무도 안 보게 된다.
    docs = {}
    for rel in ["references", "install", ""]:
        d = os.path.join(SKILL_DIR, rel) if rel else SKILL_DIR
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            key = f"{rel}/{fn}" if rel else fn
            docs[key] = open(os.path.join(d, fn), encoding="utf-8").read()

    joined = "\n".join(py.values())
    dead = []

    def walk(d, pre=""):
        for k, v in d.items():
            if k.startswith("_"):
                continue
            path = f"{pre}.{k}" if pre else k
            if isinstance(v, dict):
                walk(v, path)
            elif f'"{k}"' not in joined:
                dead.append(f"{path} = {v!r}")

    walk(cfg)

    bad = []
    # (b-1) 색상 헥스코드가 코드·문서에 리터럴로
    for key, val in cfg["colors"].items():
        if key.startswith("_") or not val:
            continue
        for name, src in list(py.items()) + list(docs.items()):
            if re.search(rf"\b{val}\b", src):
                bad.append(f"{name}: 색상 '{val}' 리터럴 — colors.{key} 하드코딩")

    # (b-2) 내 사업자번호가 코드·문서에 리터럴로
    raw = cfg["my_biz"]["biz_no"]
    for pat in (raw, f"{raw[:3]}-{raw[3:5]}-{raw[5:]}"):
        for name, src in list(py.items()) + list(docs.items()):
            if pat in src:
                bad.append(f"{name}: 사업자번호 '{pat}' 리터럴 — my_biz.biz_no 하드코딩")

    # (b-3) 월 범위 고정값. as_of.month 를 안 쓰고 숫자를 박은 경우.
    for name, src in py.items():
        for mth in re.findall(r"range\(\s*1\s*,\s*(\d+)\s*\)", src):
            bad.append(f"{name}: 'range(1, {mth})' — 월 범위 고정값 의심")

    # (b-4) 발급기한·경과일이 문서에 숫자로.
    # '개월' 단위는 보지 않는다. "홈택스는 3개월씩만 조회된다" 같은 config 와
    # 무관한 사실과 충돌해서 오탐만 늘린다.
    nums = {"grace.deadline_day": cfg["grace"]["deadline_day"],
            "thresholds.stale_days": cfg["thresholds"]["stale_days"]}
    for name, src in docs.items():
        for key, val in nums.items():
            if re.search(rf"(?<![0-9]){val}\s*일", src):
                bad.append(f"{name}: '{val}일' — {key} 를 문서에 다시 적음")

    if dead:
        rec(FAIL, f"config 죽은 키 {len(dead)}개",
            "코드가 한 번도 읽지 않는 설정이다. 바꿔도 아무 일이 안 일어난다.\n" +
            "\n".join(dead))
    else:
        rec(PASS, "config 죽은 키", "모든 설정값이 코드에서 읽힘")

    if bad:
        rec(FAIL, f"단일 출처 위반 {len(bad)}곳", "\n".join(sorted(set(bad))))
    else:
        rec(PASS, "임계값·색상 단일 출처",
            f"스크립트 {len(py)}개 · 문서 {len(docs)}개에 하드코딩 없음")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("--uploads", default="/mnt/user-data/uploads")
    ap.add_argument("--as-of", default=None)
    ap.add_argument("--strict", action="store_true",
                    help="build_report.py 를 --strict 로 만든 산출물을 검증할 때. "
                         "빼먹으면 '기한 전' 0건을 유예 로직 고장으로 오판해 FAIL 이 난다")
    a = ap.parse_args()
    as_of = date.fromisoformat(a.as_of) if a.as_of else date.today()

    cfg = load_config()
    if a.strict:
        cfg["grace"]["mode"] = "strict"
    vendors = load_vendors()
    wb = load_workbook(a.xlsx)
    df, _ = load_uploads(a.uploads, cfg)
    match_offsets(df, cfg)
    df = clip_period(df[df["받는자번호"] == cfg["my_biz"]["biz_no"]],
                     month_range(as_of), as_of)
    drop_split_offsets(df)      # build_report 와 같은 규칙을 써야 대사가 맞는다

    check_paths(cfg)
    check_config_single_source(cfg)
    check_sheets(wb, cfg)
    check_matrix_months(wb, cfg, as_of)
    check_matrix_blank_and_fill(wb, cfg, as_of)
    check_vendor_coverage(wb, cfg, vendors)
    check_totals(wb, cfg, df)
    check_monthly_totals(wb, cfg, as_of)
    check_raw_rows(wb, cfg, df)
    check_no_duplicates(wb, cfg)
    check_offsets(wb, cfg)
    check_unlisted(wb, cfg, vendors)
    check_grades(wb, cfg, vendors)
    check_state(wb, cfg)
    check_resolved(wb, cfg)
    check_grace(wb, cfg, as_of)

    print(f"\n산출물 검증 · {os.path.basename(a.xlsx)} · 기준일 {as_of}\n" + "=" * 68)
    for lv, n, d in _res:
        print(f"[{lv}] {n}")
        if d:
            for line in str(d).splitlines():
                print(f"       {line}")
    f = sum(1 for lv, _, _ in _res if lv == FAIL)
    s = sum(1 for lv, _, _ in _res if lv == SKIP)
    print("=" * 68)
    print(f"FAIL {f} · SKIP {s} · PASS {len(_res)-f-s}")
    if f:
        print("\nFAIL 이 있으면 산출물을 사용자에게 주지 말 것.")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
