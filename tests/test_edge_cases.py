"""
엣지케이스 회귀 테스트. 스킬을 고친 뒤 반드시 돌린다.

    python tests/test_edge_cases.py

여기 있는 케이스는 전부 '조용히 틀린 값이 나올 수 있었던' 실제 상황이다.
크래시보다 그럴듯한 오답이 더 위험하므로, 값까지 확인한다.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
FIX = os.path.join(HERE, "fixtures")

from common import (load_config, load_uploads, match_offsets, live_rows,  # noqa: E402
                    month_range, is_in_grace, biz_checksum_ok, norm_biz,
                    deadline_for)

fails = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        fails.append(name)


def run(args, cwd=SKILL):
    return subprocess.run([sys.executable] + args, cwd=cwd,
                          capture_output=True, text=True)


# ---------------------------------------------------------------- 단위

def t_biz():
    print("\n[사업자번호]")
    check("체크섬 통과", biz_checksum_ok("239-86-03249"))
    check("체크섬 오타 탐지", not biz_checksum_ok("239-86-03248"))
    check("전각 숫자 정규화", norm_biz("２３９８６０３２４９") == "2398603249")
    check("자릿수 부족 거부", not biz_checksum_ok("12345"))


def t_months():
    print("\n[월 범위 · 유예]")
    check("1월 실행시 1개월", month_range(date(2027, 1, 5)) == [1])
    check("10월 실행시 10개월", len(month_range(date(2026, 10, 2))) == 10)
    check("12월 실행시 12개월", len(month_range(date(2026, 12, 31))) == 12)
    cfg = load_config()
    check("12월분 기한은 익년 1월", deadline_for(2026, 12, 10) == date(2027, 1, 10))
    check("9/6 기준 8월분은 유예", is_in_grace(2026, 8, date(2026, 9, 6), cfg))
    check("9/15 기준 8월분은 확정", not is_in_grace(2026, 8, date(2026, 9, 15), cfg))
    cfg2 = dict(cfg)
    cfg2["grace"] = dict(cfg["grace"], mode="strict")
    check("strict 모드는 유예 없음", not is_in_grace(2026, 8, date(2026, 9, 6), cfg2))


def t_empty_frames():
    print("\n[빈 데이터 · 전액취소]")
    cfg = load_config()
    df, _ = load_uploads(FIX, cfg)
    match_offsets(df, cfg)
    check("빈 DataFrame 에 live_rows", len(live_rows(df.iloc[0:0])) == 0)

    # 전 건이 상계된 거래처: 최종수취일이 취소일로 새어나오면 안 된다
    g = df[(df["공급자번호"] == "2120459010") & (df["월"] >= 4)]
    lv = live_rows(g)
    check("전액취소 거래처는 유효건 0", len(lv) == 0)
    last = lv["작성일"].max().date() if len(lv) else None
    check("전액취소 거래처 최종수취일은 None", last is None,
          "취소된 날짜를 최종수취일로 쓰면 조용한 오답")

    only_neg = df[df["공급가액n"] < 0].head(3)
    check("마이너스만 있는 집합도 처리", len(live_rows(only_neg)) >= 0)


def t_kind_detection():
    print("\n[파일 종류 판정]")
    cfg = load_config()
    with tempfile.TemporaryDirectory() as d:
        # 파일명을 완전히 바꿔도 컬럼 구성으로 맞춰야 한다
        for i, f in enumerate(sorted(os.listdir(FIX))):
            shutil.copy(os.path.join(FIX, f), os.path.join(d, f"zzz_{i}.xls"))
        df, meta = load_uploads(d, cfg)
        kinds = sorted({m["kind"] for m in meta})
        check("파일명 무관 세/계 판정", kinds == ["계", "세"],
              f"판정 결과 {kinds}")


def t_offset_no_miss_match():
    print("\n[상계 오매칭]")
    cfg = load_config()
    df, _ = load_uploads(FIX, cfg)
    pairs = match_offsets(df, cfg)
    check("상계쌍이 잡힘", pairs > 0, f"{pairs}쌍")
    paired = df[df["상계"].str.contains("상계")]
    # 매월 동일 금액인 케이티가 잘못 엮이지 않았는지
    kt = paired[paired["공급자번호"] == "1028142945"]
    check("동일금액 반복 거래처 오매칭 없음", len(kt) == 0)
    for _, r in paired[paired["상계"] == "취소분(상계)"].iterrows():
        mate = paired[(paired["공급자번호"] == r["공급자번호"]) &
                      (paired["공급가액n"] == -r["공급가액n"]) &
                      (paired["상계"] == "원본(상계됨)")]
        check(f"상계쌍 품목 일치 {r['상호']}",
              len(mate) and str(mate.iloc[0].get("품목명")) == str(r.get("품목명")))
        break


# ---------------------------------------------------------------- 통합

def t_run_variants():
    print("\n[실행 변형]")
    with tempfile.TemporaryDirectory() as out:
        base = ["scripts/build_report.py", "--uploads", FIX, "--out", out, "--no-state"]

        r = run(base + ["--as-of", "2026-09-06"])
        check("기본 실행", r.returncode == 0, r.stderr.strip()[-200:])

        r2 = run(base + ["--as-of", "2026-09-06", "--strict"])
        check("strict 모드 실행", r2.returncode == 0, r2.stderr.strip()[-200:])
        check("strict 는 '기한 전' 0건", "기한 전 0" in r2.stdout, r2.stdout.strip()[-120:])

        r3 = run(base + ["--as-of", "2026-01-15"])
        check("1월 초 실행(대상 1개월)", r3.returncode == 0, r3.stderr.strip()[-200:])
        check("1월 실행시 월 범위 1", "1~1월" in r3.stdout, r3.stdout.strip()[:80])

        r4 = run(base + ["--as-of", "2026-12-31"])
        check("연말 실행(대상 12개월)", r4.returncode == 0 and "1~12월" in r4.stdout)


def t_single_kind():
    print("\n[세금계산서만 / 계산서만]")
    cfg = load_config()
    for keep, label in [("세금", "세금계산서만"), ("계산서목록", "계산서만")]:
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as out:
            for f in os.listdir(FIX):
                if (keep in f) if keep == "세금" else ("세금" not in f):
                    shutil.copy(os.path.join(FIX, f), os.path.join(d, f))
            n = len(os.listdir(d))
            r = run(["scripts/build_report.py", "--uploads", d, "--out", out,
                     "--no-state", "--as-of", "2026-09-06"])
            check(f"{label} ({n}개) 실행", r.returncode == 0, r.stderr.strip()[-200:])


def t_empty_vendors():
    print("\n[vendors.json 이 빈 경우]")
    p = os.path.join(SKILL, "config", "vendors.json")
    backup = open(p, encoding="utf-8").read()
    try:
        json.dump({"vendors": []}, open(p, "w", encoding="utf-8"))
        with tempfile.TemporaryDirectory() as out:
            r = run(["scripts/build_report.py", "--uploads", FIX, "--out", out,
                     "--no-state", "--as-of", "2026-09-06"])
            check("빈 목록으로도 실행됨", r.returncode == 0, r.stderr.strip()[-200:])
            check("전부 대상외로 분류", "점검대상 0곳" in r.stdout, r.stdout.strip()[-160:])
        r2 = run(["scripts/check_input.py", FIX, "--as-of", "2026-09-06"])
        check("check_input 이 빈 목록 경고", "비어 있음" in r2.stdout)
    finally:
        open(p, "w", encoding="utf-8").write(backup)


def t_missing_vendor_in_data():
    print("\n[자료에 한 건도 없는 거래처]")
    p = os.path.join(SKILL, "config", "vendors.json")
    backup = open(p, encoding="utf-8").read()
    try:
        d = json.loads(backup)
        d["vendors"].append({"biz_no": "1048119147", "name": "테스트 유령업체",
                             "cycle": "매월", "note": "엣지케이스 테스트용"})
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        with tempfile.TemporaryDirectory() as out:
            r = run(["scripts/build_report.py", "--uploads", FIX, "--out", out,
                     "--no-state", "--as-of", "2026-09-06"])
            check("0건 거래처 있어도 실행", r.returncode == 0, r.stderr.strip()[-300:])
            files = os.listdir(out)
            if files:
                from openpyxl import load_workbook
                wb = load_workbook(os.path.join(out, files[0]))
                ws = wb[load_config()["sheets"]["missing"]]
                txt = "\n".join(str(c.value) for row in ws.iter_rows() for c in row)
                check("0건 거래처가 '한 건도 없음'으로 잡힘", "한 건도 없음" in txt)
                check("유령업체가 목록에 등장", "테스트 유령업체" in txt)
    finally:
        open(p, "w", encoding="utf-8").write(backup)


def t_state_cycle():
    print("\n[직전 실행 비교]")
    sp = os.path.join(SKILL, "state", "last-run.json")
    backup = open(sp, encoding="utf-8").read() if os.path.exists(sp) else None
    try:
        if os.path.exists(sp):
            os.remove(sp)
        with tempfile.TemporaryDirectory() as out:
            r1 = run(["scripts/build_report.py", "--uploads", FIX, "--out", out,
                      "--as-of", "2026-09-06"])
            check("1회차 실행", r1.returncode == 0, r1.stderr.strip()[-200:])
            check("상태 파일 생성", os.path.exists(sp))
            first = json.load(open(sp, encoding="utf-8"))
            check("flagged 기록됨", len(first["flagged"]) > 0,
                  f"{len(first['flagged'])}건")
            check("first_seen 기록됨",
                  all("first_seen" in x for x in first["flagged"]))

            r2 = run(["scripts/build_report.py", "--uploads", FIX, "--out", out,
                      "--as-of", "2026-10-06"])
            check("2회차 실행", r2.returncode == 0, r2.stderr.strip()[-200:])
            from openpyxl import load_workbook
            f = sorted(os.listdir(out))[-1]
            wb = load_workbook(os.path.join(out, f))
            ws = wb[load_config()["sheets"]["missing"]]
            txt = "\n".join(str(c.value) for row in ws.iter_rows() for c in row)
            check("'계속' 상태 표시됨", "계속" in txt)
    finally:
        if backup is not None:
            open(sp, "w", encoding="utf-8").write(backup)
        elif os.path.exists(sp):
            os.remove(sp)


def main():
    print("=" * 68)
    print("엣지케이스 테스트")
    print("=" * 68)
    for fn in [t_biz, t_months, t_empty_frames, t_kind_detection,
               t_offset_no_miss_match, t_run_variants, t_single_kind,
               t_empty_vendors, t_missing_vendor_in_data, t_state_cycle]:
        try:
            fn()
        except Exception as e:
            print(f"  FAIL  {fn.__name__} 예외: {type(e).__name__}: {e}")
            fails.append(fn.__name__)
    print("\n" + "=" * 68)
    print(f"실패 {len(fails)}건" + (f": {fails}" if fails else " — 전부 통과"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
