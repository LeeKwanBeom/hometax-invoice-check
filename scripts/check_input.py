"""
업로드 파일 사전 검증. build_report.py 보다 먼저 돌린다.

가장 중요한 검사는 '기간 연속성'이다. 홈택스는 한 번에 3개월씩만 받아지는데
한 구간을 빼먹으면 리포트가 오류 없이 정상 생성되고 그럴듯하게 틀린다.
(예: 4~6월 파일을 안 올리면 전 거래처가 4~6월 미수취로 나온다.)

사용법:
    python scripts/check_input.py /mnt/user-data/uploads [--as-of YYYY-MM-DD]
종료코드 1 = 진행 불가. 0 = 진행 가능(경고는 있을 수 있음).
"""
import argparse
import sys
from datetime import date, timedelta

import pandas as pd

from common import (load_config, load_vendors, load_uploads, norm_biz, fmt_biz,
                    biz_checksum_ok, month_range)

OK, WARN, FAIL = "OK  ", "WARN", "FAIL"
_results = []


def rec(level, title, detail=""):
    _results.append((level, title, detail))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("upload_dir", nargs="?", default="/mnt/user-data/uploads")
    ap.add_argument("--as-of", default=None)
    a = ap.parse_args()
    as_of = date.fromisoformat(a.as_of) if a.as_of else date.today()

    cfg = load_config()
    vendors = load_vendors()
    df, meta = load_uploads(a.upload_dir, cfg)

    check_files(meta, df)
    check_receiver(df, cfg)
    check_continuity(df, as_of, cfg)
    check_totals(df, meta)
    check_duplicates(df)
    check_vendors(vendors, df)

    print(f"\n입력 검증 · 기준일 {as_of}\n" + "=" * 68)
    for lv, t, d in _results:
        print(f"[{lv}] {t}")
        if d:
            for line in str(d).splitlines():
                print(f"       {line}")
    fails = sum(1 for lv, _, _ in _results if lv == FAIL)
    warns = sum(1 for lv, _, _ in _results if lv == WARN)
    print("=" * 68)
    print(f"FAIL {fails} · WARN {warns} · 총 {len(df)}건 / 공급자 {df['공급자번호'].nunique()}곳")
    if fails:
        print("\nFAIL 이 있으면 리포트를 만들지 말 것. 위 내용을 사용자에게 먼저 알린다.")
    return 1 if fails else 0


def check_files(meta, df):
    kinds = {m["kind"] for m in meta}
    lines = [f"{m['file']} · {m['kind']} · {m['rows']}건" for m in meta]
    rec(OK, f"파일 {len(meta)}개 읽음", "\n".join(lines))
    if "세" not in kinds:
        rec(WARN, "전자세금계산서 파일이 없음", "계산서만으로 점검하면 대부분 거래가 빠진다.")
    if "계" not in kinds:
        rec(WARN, "전자계산서 파일이 없음", "면세 매입(농축수산물 등)이 통째로 빠진다.")


def check_receiver(df, cfg):
    """매출분이 섞여 있으면 제외하고 몇 건인지 보고한다."""
    mine = cfg["my_biz"]["biz_no"]
    bad = df[df["받는자번호"] != mine]
    if len(bad):
        by = bad.groupby("받는자번호").size().to_dict()
        rec(WARN, f"공급받는자가 내 사업장이 아닌 건 {len(bad)}건 — 제외 대상",
            "\n".join(f"{fmt_biz(k)} · {v}건" for k, v in by.items()))
    else:
        rec(OK, f"전 건이 내 사업장({fmt_biz(mine)}) 매입분 — 매출분 제외 0건")


def check_continuity(df, as_of, cfg):
    """
    파일들이 덮는 날짜 구간에 구멍이 있는지 본다.
    작성일자가 하루도 없는 '빈 달'이 중간에 있으면 파일 누락을 의심한다.
    """
    year = as_of.year
    cur = df[df["연"] == year]
    if len(cur) == 0:
        rec(FAIL, f"{year}년 작성분이 한 건도 없음", "다른 연도 파일을 올렸을 수 있다.")
        return

    months = set(cur["월"])
    want = month_range(as_of)
    gap = [m for m in want if m not in months]
    # 실행월은 아직 데이터가 없는 게 정상
    gap = [m for m in gap if m != as_of.month]

    if gap:
        rec(FAIL, f"{year}년 {', '.join(str(m) + '월' for m in gap)} 데이터가 통째로 없음",
            "홈택스 파일 한 구간을 빼먹었을 가능성이 높다.\n"
            "그대로 진행하면 전 거래처가 해당 월 미수취로 잘못 나온다.\n"
            "정말 거래가 없던 달이라면 이 경고를 무시해도 된다.")
    else:
        rec(OK, f"{year}년 1~{max(months)}월 연속 — 구간 누락 없음")

    other = sorted(set(df["연"]) - {year})
    if other:
        rec(WARN, f"{year}년 외 작성분 포함: {other}",
            "점검 기간(당해 1/1~오늘) 밖이라 집계에서 제외된다.")


def check_totals(df, meta):
    """홈택스 파일 헤더의 '총 공급가액' 과 실제 합산값을 대사한다."""
    lines, bad = [], False
    for m in meta:
        if m["declared_total"] is None:
            lines.append(f"{m['file']} · 헤더 총계 없음(건너뜀)")
            continue
        got = int(df[df["원본파일"] == m["file"]]["공급가액n"].sum())
        mark = "일치" if got == m["declared_total"] else "불일치"
        if got != m["declared_total"]:
            bad = True
        lines.append(f"{m['file']} · 헤더 {m['declared_total']:,} / 합산 {got:,} · {mark}")
    rec(FAIL if bad else OK, "헤더 총계 대사", "\n".join(lines))


def check_duplicates(df):
    dup = df[df["승인번호"].duplicated(keep=False)]
    if len(dup):
        rec(FAIL, f"승인번호 중복 {len(dup)}건",
            "같은 구간 파일을 두 번 올렸을 수 있다. 중복분을 빼고 다시 올릴 것.\n" +
            "\n".join(dup["승인번호"].unique()[:10]))
    else:
        rec(OK, "승인번호 중복 없음")


def check_vendors(vendors, df):
    """vendors.json 자체의 건강 상태."""
    if not vendors:
        rec(WARN, "점검 대상 거래처 목록이 비어 있음",
            "config/vendors.json 이 비면 '미수취' 판정이 나오지 않는다.\n"
            "자료에 등장한 공급자 전체가 '대상외'로만 분류된다.")
        return

    bad = [v for v in vendors if not biz_checksum_ok(v["biz_no"])]
    if bad:
        rec(FAIL, f"vendors.json 사업자번호 체크섬 오류 {len(bad)}건",
            "오타가 있으면 그 거래처는 영영 '한 건도 없음'으로 잡힌다.\n" +
            "\n".join(f"{fmt_biz(v['biz_no'])} {v['name']}" for v in bad))
    else:
        rec(OK, f"점검 대상 거래처 {len(vendors)}곳 · 사업자번호 체크섬 정상")

    seen = {}
    for v in vendors:
        seen.setdefault(norm_biz(v["biz_no"]), []).append(v["name"])
    dups = {k: n for k, n in seen.items() if len(n) > 1}
    if dups:
        rec(WARN, "vendors.json 에 같은 사업자번호 중복 등록",
            "\n".join(f"{fmt_biz(k)} · {' / '.join(n)}" for k, n in dups.items()))

    # 상호는 같은데 사업자번호가 다른 경우 = 사업자 변경 가능성
    alias = {}
    for sid, g in df.groupby("공급자번호"):
        nm = str(g["상호"].iloc[-1]).replace(" ", "").replace("주식회사", "").replace("(주)", "")
        alias.setdefault(nm, set()).add(sid)
    changed = {k: v for k, v in alias.items() if len(v) > 1}
    if changed:
        rec(WARN, "같은 상호인데 사업자번호가 다름 — 사업자 변경 가능성",
            "\n".join(f"{k} · {' / '.join(fmt_biz(x) for x in sorted(v))}"
                      for k, v in changed.items()) +
            "\n변경이라면 vendors.json 에서 구 번호를 지우고 신 번호로 교체할 것.")


if __name__ == "__main__":
    sys.exit(main())
