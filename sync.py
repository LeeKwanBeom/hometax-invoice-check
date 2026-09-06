"""
저장소에서 스킬 코드·설정을 작업 디렉토리로 내려받는다.

이 스크립트만 SKILL.md 의 curl 한 줄로 받아오면 나머지는 여기서 처리한다.
컨테이너가 초기화되어도, 다른 컴퓨터에서 실행해도 항상 저장소 최신본을 쓴다.

## 왜 tarball 인가

raw.githubusercontent.com 은 **5분간 캐시된다**(`cache-control: max-age=300`).
push.py 로 코드를 올린 직후 다시 sync 하면 옛 파일이 내려온다.
`?t=타임스탬프` 같은 캐시버스터도 통하지 않는다.

codeload 의 tarball 은 캐시되지 않고, 요청 한 번으로 저장소 전체를 받는다.
파일별로 18번 요청하던 것보다 빠르고, 중간에 일부만 받아지는 일도 없다.

사용법:
    python3 sync.py [작업디렉토리] [--token TOKEN] [--ref main|<커밋SHA>]
"""
import argparse
import io
import os
import shutil
import sys
import tarfile
import urllib.error
import urllib.request

REPO = "LeeKwanBeom/hometax-invoice-check"
BRANCH = "main"

# 작업 디렉토리에 풀지 않을 것.
# README.md 와 SKILL.md 는 push --code 로 갱신할 수 있게 받아둔다.
# 여기 받아지는 SKILL.md 는 '저장소 사본'이다. 고친 뒤 push 하면 버전은 남지만,
# Claude 계정에 설치된 SKILL.md 는 사용자가 직접 재업로드해야 바뀐다.
SKIP = {".gitignore"}
SKIP_PREFIX = (".github/",)


def fetch_tarball(ref, token):
    url = f"https://codeload.github.com/{REPO}/tar.gz/{ref}"
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise SystemExit(
                f"[중단] 저장소나 브랜치를 찾을 수 없습니다 (404).\n"
                f"       {REPO} @ {ref}\n"
                f"       저장소가 공개인지, 파일이 올라가 있는지 확인하세요.\n"
                f"       비공개 저장소라면 --token 이 필요합니다."
            )
        raise SystemExit(f"[중단] 다운로드 실패 HTTP {e.code}\n       {url}")
    except Exception as e:
        raise SystemExit(
            f"[중단] 네트워크 오류: {e}\n"
            f"       codeload.github.com 접근이 막혀 있으면 설정에서 허용해야 합니다."
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dest", nargs="?", default=None)
    ap.add_argument("--token", default=None, help="비공개 저장소일 때만 필요")
    ap.add_argument("--ref", default=f"refs/heads/{BRANCH}",
                    help="브랜치 또는 커밋 SHA. 기본 main")
    # 예전 버전 호환. tarball 은 어차피 전부 받으므로 무시한다.
    ap.add_argument("--with-tests", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()

    dest = os.path.abspath(a.dest) if a.dest else os.getcwd()
    os.makedirs(dest, exist_ok=True)

    print(f"저장소: {REPO} @ {a.ref}")
    print(f"대상:   {dest}\n")

    blob = fetch_tarball(a.ref, a.token)
    print(f"  받음  {len(blob):,}B (압축)")

    written, skipped = [], []
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile()]
        if not members:
            raise SystemExit("[중단] 압축 파일이 비어 있습니다. 저장소를 확인하세요.")
        # 최상위 디렉토리(<repo>-<ref>/) 를 벗겨낸다
        root = members[0].name.split("/")[0] + "/"

        for m in members:
            rel = m.name[len(root):] if m.name.startswith(root) else m.name
            if not rel or rel in SKIP or rel.startswith(SKIP_PREFIX):
                skipped.append(rel)
                continue
            # 경로 탈출 방어
            full = os.path.normpath(os.path.join(dest, rel))
            if not full.startswith(os.path.normpath(dest) + os.sep):
                raise SystemExit(f"[중단] 비정상 경로: {rel}")
            os.makedirs(os.path.dirname(full), exist_ok=True)
            src = tf.extractfile(m)
            if src is None:
                continue
            with open(full, "wb") as f:
                shutil.copyfileobj(src, f)
            written.append((rel, m.size))

    written.sort()
    for rel, size in written:
        print(f"        {rel}  ({size:,}B)")

    need = ["config/check-config.json", "config/vendors.json",
            "scripts/common.py", "scripts/build_report.py",
            "scripts/check_input.py", "scripts/validate.py", "scripts/push.py"]
    missing = [p for p in need if not os.path.exists(os.path.join(dest, p))]
    if missing:
        raise SystemExit(f"\n[중단] 필수 파일이 없습니다: {missing}\n"
                         f"       저장소에 제대로 올라갔는지 확인하세요.")

    print(f"\n{len(written)}개 파일 · 준비 완료")
    print(f"다음: cd {dest} && python3 scripts/check_input.py /mnt/user-data/uploads")


if __name__ == "__main__":
    main()
