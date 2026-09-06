---
name: hometax-invoice-check
description: 홈택스 매입 전자세금계산서·전자계산서 목록을 받아, 거래처가 세금계산서를 빠뜨리고 안 보낸 곳이 있는지 점검해 엑셀 리포트를 만든다. "세금계산서 점검", "매입 세금계산서 확인", "미수취 확인", "계산서 안 온 곳", "세금계산서 누락", "홈택스 매입 점검", "부가세 자료 점검", "세금계산서 스킬" 같은 말이 나오거나, 홈택스 매입 목록 xls(매입전자세금계산서목록_*.xls / 매입전자계산서목록_*.xls)가 업로드되면 반드시 이 스킬을 사용할 것. 거래처별 월별 수취 매트릭스, 미수취 의심 목록, 발급기한 임박 확인, 거래처 목록(vendors) 관리에 적용된다.
---

# 매입 세금계산서 수취 점검 — 부트스트랩

**이 파일은 설명서가 아니다. 진짜 설명서를 받아오는 안내문이다.**

절차·명령어·옵션·등급 이름은 여기 없다. 전부 저장소에 있다.
이 파일에 그런 걸 적으면 반드시 낡는다 — 설치 경로는 세션마다
패키지에서 다시 풀리므로, 여기 쓴 수정은 다음 세션에 사라진다.
(2026-09-06 실측: 전날 덮어쓴 SKILL.md 가 옛 버전으로 되돌아가 있었다.)

## 1. 저장소를 받는다

```bash
mkdir -p /home/claude/hometax && cd /home/claude/hometax
curl -sL https://codeload.github.com/LeeKwanBeom/hometax-invoice-check/tar.gz/refs/heads/main | tar xz --strip-components=1
python3 -c "import xlrd" 2>/dev/null || pip install xlrd --break-system-packages -q
ls
```

`config/`, `references/`, `scripts/`, `state/`, `tests/` 가 보이면 성공이다.

받아지지 않으면:
- 404 → 저장소가 비공개로 바뀌었거나 브랜치명이 다르다. 사용자에게 알린다
- 네트워크 오류 → `codeload.github.com` 접근이 막힌 것이다. 설정에서 허용해야 한다

**받지 못하면 그 지점에서 멈추고 사용자에게 알린다.** 기억으로 절차를
지어내지 말 것. 이 파일에는 판정 논리도 임계값도 없다.

## 2. 받은 설명서를 읽고 그대로 따른다

```
/home/claude/hometax/SKILL.md          ← 실제 설명서. 이걸 따른다
/home/claude/hometax/audit/last-audit.md   ← 있으면 함께 읽는다
```

`audit/last-audit.md` 는 직전 점검 기준선이다. 알려진 미해결 결함과
"다음 점검에서 먼저 볼 것" 이 적혀 있다. 스킬을 고치거나 결과가
이상해 보일 때 **먼저 여기를 본다.** 이미 알려진 문제를 다시 찾느라
시간을 쓰지 않기 위해서다.

## 3. 이 파일을 고치지 말 것

내용을 바꿔야 하면:

| 무엇 | 어디에 | 어떻게 |
|---|---|---|
| 절차·옵션·등급 등 설명서 내용 | 저장소 `SKILL.md` | `python3 scripts/push.py <토큰> --code` |
| 이 부트스트랩 문구 자체 | 저장소 `install/SKILL.md` | 위와 같이 push 한 뒤, **사용자가 Claude 설정에서 스킬을 재업로드해야** 실제로 반영된다 |

설치 경로(`/mnt/skills/plugins/hometax-invoice-check/`)에 직접 쓰는 것은
쓰기는 되지만 **보존되지 않는다.** 사용자에게 재업로드가 필요하다고 알린다.
