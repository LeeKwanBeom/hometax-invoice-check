"""
바뀐 파일을 저장소에 되돌려 올린다.

올리지 않으면 다음 실행 때 sync.py 가 저장소 버전으로 덮어써서 수정이 사라진다.
대화 안에서 고친 것은 컨테이너와 함께 없어지므로, 이 스크립트가 유일한 저장 경로다.

세 묶음으로 나눠 올린다.

  state    state/last-run.json          실행할 때마다 바뀜
  vendors  config/vendors.json          거래처 추가·수정할 때
  code     SKILL.md scripts/ config/check-config.json references/
           tests/ audit/ install/ sync.py README.md

기본값은 state + vendors 다. **코드를 고쳤으면 --code 를 반드시 붙인다.**

안전장치: --code 는 tests/test_edge_cases.py 를 먼저 돌리고, 실패하면 올리지 않는다.
고치다 깨진 걸 모르고 올려서 다음 달에 발견하는 상황을 막는다.
(정말 급하면 --skip-tests 로 넘길 수 있지만 권하지 않는다.)

토큰은 **저장하지 않는다.** 매번 사용자에게 받는다.
(Settings → Developer settings → Fine-grained tokens,
 hometax-invoice-check 저장소에 Contents: Read and write)

사용법:
    python3 scripts/push.py <토큰>                     # state + vendors
    python3 scripts/push.py <토큰> --code              # 코드까지 (테스트 통과 시)
    python3 scripts/push.py <토큰> --code --dry-run    # 뭐가 바뀌었는지만 확인
    python3 scripts/push.py <토큰> --only vendors
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

REPO = "LeeKwanBeom/hometax-invoice-check"
BRANCH = "main"
API = f"https://api.github.com/repos/{REPO}/contents"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROUPS = {
    "state": ["state/last-run.json"],
    "vendors": ["config/vendors.json"],
    "code": [
        "SKILL.md",
        "sync.py",
        "README.md",
        "config/check-config.json",
        "references/column-mapping.md",
        "references/judgment-rules.md",
        "references/excel-format.md",
        "scripts/common.py",
        "scripts/check_input.py",
        "scripts/build_report.py",
        "scripts/validate.py",
        "scripts/push.py",
    ],
}


def _scan(rel):
    """
    디렉토리 안의 파일을 code 묶음에 통째로 넣는다.

    목록에 하드코딩하면 새 파일을 만들어도 영영 저장소에 안 올라가고,
    다음 sync 때 옛 상태로 덮여 되돌아간다. 테스트 픽스처가 실제로 그랬다.
    없는 디렉토리는 빈 목록이라 그냥 건너뛴다.
    """
    d = os.path.join(ROOT, *rel.split("/"))
    if not os.path.isdir(d):
        return []
    out = []
    for base, _, files in os.walk(d):
        for f in sorted(files):
            if f.startswith("."):
                continue
            full = os.path.join(base, f)
            out.append(os.path.relpath(full, ROOT).replace(os.sep, "/"))
    return sorted(out)


# tests/ = 테스트 코드와 픽스처, audit/ = 점검 이력 메모(last-audit.md 등),
# install/ = 설치용 얇은 부트스트랩 SKILL.md.
# 파일명을 하나씩 적어두면 새로 만든 파일이 조용히 빠진다. 통째로 훑는다.
GROUPS["code"] += _scan("tests") + _scan("audit") + _scan("install")


# ---------------------------------------------------------------- GitHub API

def api(method, url, token, payload=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    body = json.dumps(payload).encode() if payload is not None else None
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, body, timeout=30) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        if e.code == 404 and method == "GET":
            return None
        if e.code == 404:
            raise SystemExit(
                f"[중단] 저장소를 찾을 수 없습니다 (404).\n"
                f"       {REPO} 가 실제로 존재하는지, 토큰이 그 저장소에\n"
                f"       접근 권한을 갖고 있는지 확인하세요."
            )
        if e.code in (401, 403):
            raise SystemExit(
                f"[중단] 토큰 권한 오류 (HTTP {e.code}).\n"
                f"       {REPO} 에 Contents: Read and write 권한이 있는지,\n"
                f"       토큰이 만료되지 않았는지 확인하세요.\n       {detail}"
            )
        if e.code == 409:
            raise SystemExit(
                "[중단] 저장소가 그 사이에 바뀌었습니다 (409).\n"
                "       sync.py 를 다시 돌려 최신본을 받은 뒤, 수정을 다시 적용하고 올리세요."
            )
        raise SystemExit(f"[중단] GitHub API 오류 HTTP {e.code}\n       {detail}")
    except Exception as e:
        raise SystemExit(
            f"[중단] 네트워크 오류: {e}\n"
            f"       api.github.com 접근이 막혀 있으면 설정에서 허용해야 합니다."
        )


def remote(path, token):
    url = f"{API}/{urllib.request.quote(path)}?ref={BRANCH}"
    cur = api("GET", url, token)
    if not cur:
        return None, None
    return cur.get("sha"), base64.b64decode(cur.get("content", ""))


def put(path, content, sha, token, message):
    payload = {"message": message,
               "content": base64.b64encode(content).decode(),
               "branch": BRANCH}
    if sha:
        payload["sha"] = sha
    api("PUT", f"{API}/{urllib.request.quote(path)}", token, payload)


# ---------------------------------------------------------------- 비교

def same(a, b):
    """줄바꿈 차이(CRLF/LF)는 변경으로 보지 않는다."""
    if a is None or b is None:
        return False
    return a.replace(b"\r\n", b"\n") == b.replace(b"\r\n", b"\n")


def state_regressed(old, new):
    """
    sync 하지 않은 폴더에서 push 하면 원격의 최신 이력을 옛 것으로 덮어쓴다.
    월 1~2회 · 여러 컴퓨터로 쓰는 스킬에서 실제로 밟기 쉬운 함정이라 막는다.
    """
    try:
        n = json.loads(new.decode())
    except Exception as e:
        return f"로컬 이력 파일을 읽을 수 없습니다 ({e})"
    if not old:
        return None
    try:
        o = json.loads(old.decode())
    except Exception:
        # 원격이 깨졌으면 '되돌아가는지' 판단할 근거가 없다.
        # 그냥 통과시키면 가드가 있으나 마나가 된다.
        return "원격 이력 파일이 깨져 있어 비교할 수 없습니다"
    od, nd = o.get("run_date"), n.get("run_date")
    if od and not nd:
        return f"원격에는 {od} 이력이 있는데 로컬은 비어 있습니다"
    if od and nd and nd < od:
        return f"원격 {od} → 로컬 {nd} 로 되돌아갑니다"
    if od and nd and nd == od:
        # 날짜만 보면 같은 날 두 번 돌린 경우를 못 잡는다. 두 번째 실행이
        # 잘못된 업로드로 돌아갔으면 원격 이력이 조용히 줄어들고,
        # 다음 달 '신규/계속/해결' 이 그만큼 어긋난다.
        of, nf = len(o.get("flagged", [])), len(n.get("flagged", []))
        if nf < of:
            return (f"같은 날짜({od})인데 확인 필요가 {of}건 → {nf}건 으로 줄어듭니다")
    return None


def diff_lines(old, new, path):
    """텍스트 파일이면 몇 줄이 바뀌었는지 요약한다."""
    if path.endswith((".xls", ".xlsx", ".png")):
        return "이진 파일"
    try:
        import difflib
        o = (old or b"").decode("utf-8").splitlines()
        n = new.decode("utf-8").splitlines()
        add = sum(1 for x in difflib.ndiff(o, n) if x.startswith("+ "))
        rem = sum(1 for x in difflib.ndiff(o, n) if x.startswith("- "))
        return f"+{add} / -{rem} 줄"
    except Exception:
        return f"{len(new):,}B"


# ---------------------------------------------------------------- 테스트 게이트

def run_tests():
    test = os.path.join(ROOT, "tests", "test_edge_cases.py")
    if not os.path.exists(test):
        print("  경고  tests/test_edge_cases.py 가 없습니다.")
        print("        python3 sync.py . 로 저장소 최신본을 받은 뒤 다시 시도하세요.")
        return False
    print("  엣지케이스 테스트 실행 중...")
    r = subprocess.run([sys.executable, "tests/test_edge_cases.py"],
                       cwd=ROOT, capture_output=True, text=True)
    tail = (r.stdout or "").strip().splitlines()[-3:]
    for line in tail:
        print(f"        {line}")
    if r.returncode != 0:
        print("\n  테스트 실패. 코드를 올리지 않습니다.")
        fails = [l for l in (r.stdout or "").splitlines() if "FAIL" in l]
        for l in fails[:12]:
            print(f"        {l}")
        return False
    return True


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("token")
    ap.add_argument("--code", action="store_true",
                    help="스크립트·설정·문서까지 올린다. 코드를 고쳤으면 필수")
    ap.add_argument("--only", choices=list(GROUPS), default=None)
    ap.add_argument("--dry-run", action="store_true", help="비교만 하고 올리지 않음")
    ap.add_argument("--skip-tests", action="store_true",
                    help="테스트 없이 코드 올리기 (권장하지 않음)")
    ap.add_argument("--message", default=None, help="커밋 메시지")
    ap.add_argument("--force", action="store_true",
                    help="실행 이력이 뒤로 가도 강행 (이력이 지워짐)")
    a = ap.parse_args()

    if a.only:
        groups = [a.only]
    else:
        groups = ["state", "vendors"] + (["code"] if a.code else [])

    print(f"저장소: {REPO}@{BRANCH}")
    print(f"묶음:   {', '.join(groups)}" + ("  (dry-run)" if a.dry_run else ""))
    print()

    # 1) 무엇이 바뀌었는지 먼저 전부 비교한다. 올리기 전에 보여주는 게 목적이다.
    changed, missing = [], []
    for gname in groups:
        for path in GROUPS[gname]:
            local = os.path.join(ROOT, path)
            if not os.path.exists(local):
                missing.append(path)
                continue
            with open(local, "rb") as f:
                content = f.read()
            sha, old = remote(path, a.token)
            if same(old, content):
                continue
            if path == "state/last-run.json":
                back = state_regressed(old, content)
                if back and not a.force:
                    raise SystemExit(
                        f"[중단] 실행 이력이 뒤로 갑니다: {back}\n"
                        f"       sync 하지 않은 폴더에서 push 하면 원격 이력이 지워집니다.\n"
                        f"       저장소에서 최신본을 받은 폴더에서 다시 실행하세요.\n"
                        f"       거래처를 의도적으로 뺐다면 줄어든 항목이\n"
                        f"       그 거래처와 일치하는지 먼저 확인하세요.\n"
                        f"       전부 설명되면 --force 가 정당합니다"
                        f" (SKILL.md '가드가 걸렸을 때 밟는 3단계')."
                    )
            changed.append((path, content, sha, "신규" if old is None
                            else diff_lines(old, content, path)))

    for p in missing:
        print(f"  없음    {p} (로컬에 없어 건너뜀)")

    if not changed:
        print("  변경 없음. 아무것도 올리지 않았습니다.")
        return 0

    print("  바뀐 파일:")
    for path, _, _, d in changed:
        print(f"    {path}  ({d})")
    print()

    # 2) 코드가 섞여 있으면 테스트를 통과해야 올린다.
    code_changed = [p for p, _, _, _ in changed if p in GROUPS["code"]]
    if code_changed and not a.skip_tests and not a.dry_run:
        if not run_tests():
            print("\n고친 부분을 확인한 뒤 다시 시도하세요.")
            print("정말 그대로 올려야 하면 --skip-tests 를 붙이되, 권하지 않습니다.")
            return 1
        print()

    if a.dry_run:
        print("dry-run 이라 올리지 않았습니다.")
        return 0

    # 3) 실제 업로드
    msg = a.message or f"update: {', '.join(p for p, _, _, _ in changed[:4])}" + \
        (" 외" if len(changed) > 4 else "")
    for path, content, sha, _ in changed:
        put(path, content, sha, a.token, msg)
        print(f"  올림    {path}")

    print(f"\n{len(changed)}개 파일 반영 완료")
    if code_changed:
        print("코드가 바뀌었으니, 다음 실행 때 sync.py 가 이 버전을 받아옵니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
