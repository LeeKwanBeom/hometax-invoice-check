"""
저장소에서 스킬 코드·설정을 작업 디렉토리로 내려받는다.

이 스크립트만 SKILL.md 의 curl 한 줄로 받아오면, 나머지는 여기서 전부 처리한다.
컨테이너가 초기화되어도, 다른 컴퓨터에서 실행해도 항상 저장소 최신본을 쓴다.

사용법:
    python3 sync.py [작업디렉토리]        # 기본 현재 디렉토리
    python3 sync.py --check              # 받아진 파일만 점검
"""
import os
import sys
import urllib.error
import urllib.request

REPO = "LeeKwanBeom/hometax-invoice-check"
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

# 저장소에서 받아올 파일. tests/fixtures 는 용량이 커서 --with-tests 일 때만 받는다.
CORE = [
    "config/check-config.json",
    "config/vendors.json",
    "references/column-mapping.md",
    "references/judgment-rules.md",
    "references/excel-format.md",
    "scripts/common.py",
    "scripts/check_input.py",
    "scripts/build_report.py",
    "scripts/validate.py",
    "scripts/push.py",
]
STATE = ["state/last-run.json"]          # 없을 수 있음(최초 실행)
TESTS = [
    "tests/test_edge_cases.py",
    "tests/fixtures/매입전자세금계산서목록_1_150_.xls",
    "tests/fixtures/매입전자세금계산서목록_1_132_.xls",
    "tests/fixtures/매입전자세금계산서목록_1_80_.xls",
    "tests/fixtures/매입전자계산서목록_1_30_.xls",
    "tests/fixtures/매입전자계산서목록_1_33_.xls",
    "tests/fixtures/매입전자계산서목록_1_16_.xls",
]


def fetch(path, dest, optional=False):
    url = f"{RAW}/{urllib.request.quote(path)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if optional and e.code == 404:
            return None
        raise SystemExit(
            f"[중단] {path} 를 받지 못했습니다 (HTTP {e.code}).\n"
            f"       {url}\n"
            f"       저장소가 공개인지, 파일이 올라가 있는지 확인하세요."
        )
    except Exception as e:
        raise SystemExit(
            f"[중단] 네트워크 오류로 {path} 를 받지 못했습니다: {e}\n"
            f"       raw.githubusercontent.com 접근이 막혀 있으면 설정에서 허용해야 합니다."
        )
    if len(data) == 0:
        raise SystemExit(f"[중단] {path} 가 0바이트입니다. 저장소 파일을 확인하세요.")
    full = os.path.join(dest, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as f:
        f.write(data)
    return len(data)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    dest = os.path.abspath(args[0]) if args else os.getcwd()
    os.makedirs(dest, exist_ok=True)

    want = list(CORE)
    if "--with-tests" in flags:
        want += TESTS

    print(f"저장소: {REPO}@{BRANCH}")
    print(f"대상:   {dest}\n")

    total = 0
    for p in want:
        n = fetch(p, dest)
        total += n
        print(f"  받음  {p}  ({n:,}B)")

    for p in STATE:
        n = fetch(p, dest, optional=True)
        if n is None:
            print(f"  없음  {p}  (최초 실행이면 정상)")
        else:
            print(f"  받음  {p}  ({n:,}B)")

    print(f"\n총 {total:,}B · 준비 완료")
    print(f"다음: cd {dest} && python3 scripts/check_input.py /mnt/user-data/uploads")


if __name__ == "__main__":
    main()
