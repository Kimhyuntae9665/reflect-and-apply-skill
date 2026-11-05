# 성찰 후 반영 · Reflect and Apply

**사용자의 정정·확인 답변을 다음 작업 전에 적용할 지침으로 바꾸는 Codex 스킬입니다.**

`기억하겠습니다`라는 답변에서 끝내지 않고, 무엇을 잘못 판단했는지 확인한 뒤 관련 지침·스킬·사실 원장을 필요한 만큼 수정하고 검증합니다. 한 문서의 예외를 모든 작업의 규칙으로 확대하지 않는 데 중점을 둡니다.

> A Korean-first Codex skill for turning user corrections and confirmed answers into scoped, verifiable instruction updates. It preserves one-off exceptions, evidence status, privacy, and existing authorization boundaries. It does not retrain a model or provide a background monitoring service.

[실행 지침](SKILL.md) · [전체 예시](references/worked-example.md) · [검증 사례](references/acceptance-cases.md) · [MIT 라이선스](LICENSE)

## 이런 요청에 사용합니다

```text
$reflect-and-apply 이번 채팅에서 내가 정정한 내용을 다음 작업 지침에 반영해줘.

$reflect-and-apply 최근 같은 질문을 반복한 원인을 확인하고,
이미 답한 값은 질문 전에 찾아서 재사용하도록 관련 지침을 고쳐줘.

$reflect-and-apply 오늘 관련 채팅을 돌아보되 분석만 해줘.
파일은 수정하지 말고 개선 후보와 적용 범위만 정리해줘.
```

단순 오탈자 하나를 고칠 때마다 전역 규칙을 추가하는 도구는 아닙니다. 현재 채팅이 기본이며, 다른 채팅은 요청과 필요성·도구 접근 범위 안에서 확인합니다.

## 무엇이 달라지나요?

| 상황 | 반영 방식 | 다음 작업에서 먼저 할 일 |
|---|---|---|
| 같은 부적절한 사례를 반복 선정 | 기존 선정 기준의 대조 행동 보강 | 실제 업무의 행동·산출물과 후보 수행 대조 |
| 이미 답한 확인 질문을 다시 함 | 해당 사실 원장과 조회 연결 갱신 | 현재 대화와 원장을 읽고 부족한 필드만 질문 |
| `이 문서만` 배치를 바꾸라고 함 | 문서별 예외를 작업 기록에 보존 | 같은 문서 재개 시 예외 유지, 다른 문서 기본값 유지 |
| 기존 규칙을 읽지 않고 누락 | 규칙을 복제하지 않고 조회 시점 수정 | 결정 전에 소유 파일을 실제로 열람 |
| 가격·공고·서비스 상태가 바뀜 | 확인 날짜와 관측 상태를 기록 | 새로 사용할 때 현재 상태 재확인 |
| 새로운 재사용 정보가 없음 | 파일 변경 없이 종료 가능 | 기존 유효 기준 그대로 적용 |

## 동작 순서

1. **근거 확보:** 사용자 발언, 앞선 질문, 실제 결과물과 기존 지침을 읽습니다.
2. **분류:** 반복 원인·지속 선호·이번 예외·확인 사실·변화하는 정보를 나눕니다.
3. **반영 위치 선택:** AGENTS, 소유 스킬, 사실 원장, 작업 기록 중 책임이 맞는 파일을 고릅니다.
4. **최소 수정:** 기존 중복과 예외를 확인하고 변경 전 상태를 보존한 뒤 관련 절만 고칩니다.
5. **검증:** diff·재열람, 실패 조건과 정상 예외, 같은 입력의 재실행을 확인합니다.
6. **다음 행동 연결:** 질문·선정·제작 전에 읽을 경로와 대조할 기준을 남깁니다.

세부 절차는 에이전트가 읽는 [SKILL.md](SKILL.md)에 있고, 긴 판단 예시와 검증 자료는 조건별 참조로 분리했습니다.

## 설치

스킬 사용 자체에는 Python 패키지나 별도 API 키가 필요하지 않습니다. 검증 도구를 실행할 때만 Python과 PyYAML이 필요합니다. Git으로 설치하려면 Git을 준비합니다.

### 방법 1: Codex에 설치 요청

`skill-installer`가 있는 환경에서 다음처럼 요청할 수 있습니다.

```text
$skill-installer https://github.com/Kimhyuntae9665/reflect-and-apply-skill
저장소 루트의 스킬을 reflect-and-apply 이름으로 설치해줘.
같은 이름이 이미 설치돼 있으면 덮어쓰지 말고 위치와 차이를 확인해줘.
```

설치 도구의 지원 방식은 환경마다 다를 수 있습니다. 이 저장소가 공식 기본 스킬 목록에 포함돼 있다는 뜻은 아닙니다.

### 방법 2: 사용자 스킬 폴더에 직접 설치

현재 공식 문서의 사용자 경로는 `~/.agents/skills`입니다. 로컬 스킬 검색 위치와 명시적/자동 호출은 [OpenAI의 Build skills 문서](https://learn.chatgpt.com/docs/build-skills)를 기준으로 안내합니다. 확인일: 2026-11-05.

**Windows PowerShell** — 대상 폴더가 이미 있으면 중단합니다.

```powershell
$skillRoot = Join-Path $env:USERPROFILE '.agents\skills'
$skillTarget = Join-Path $skillRoot 'reflect-and-apply'
if (Test-Path -LiteralPath $skillTarget) {
    throw '이미 설치된 스킬이 있습니다. 백업과 차이를 확인한 뒤 갱신하세요.'
}
New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
git clone https://github.com/Kimhyuntae9665/reflect-and-apply-skill.git $skillTarget
```

**macOS / Linux** — 대상 폴더가 이미 있으면 설치하지 않습니다.

```bash
skill_root="$HOME/.agents/skills"
skill_target="$skill_root/reflect-and-apply"
if [ -e "$skill_target" ] || [ -L "$skill_target" ]; then
  echo 'Already installed: review the existing skill before updating.' >&2
else
  mkdir -p "$skill_root"
  git clone https://github.com/Kimhyuntae9665/reflect-and-apply-skill.git "$skill_target"
fi
```

기존 환경이 별도로 지정한 스킬 경로를 사용한다면 그 경로를 우선합니다. 같은 이름을 여러 검색 위치에 중복 설치하지 마세요. 이 패키지의 진입점은 저장소 루트의 `SKILL.md`이며, 설치 폴더 이름은 `reflect-and-apply`로 둡니다.

Codex에서 `$reflect-and-apply`로 호출해 보세요. 업데이트가 보이지 않으면 Codex를 재시작하고 검색 경로·중복 설치·비활성화 설정을 확인하세요. 파일 복사만으로 실제 발견·호출이 확인된 것은 아닙니다.

## 자동 적용과 권한

`agents/openai.yaml`은 자동 선택을 허용합니다. 이는 호스트가 해당 스킬을 선택할 수 있다는 설정이며, 매 턴 자동 실행이나 모든 파일의 수정 권한을 뜻하지 않습니다.

프로젝트에서 상시 반영을 원하면 기존 `AGENTS.md`에 아래처럼 짧게 연결할 수 있습니다. **설치 과정은 AGENTS를 자동으로 수정하지 않습니다.**

```markdown
## 재사용할 피드백 반영

결과물을 실질적으로 정정했거나 재사용할 확인 답변을 받으면,
현재 결과물의 수정·검수를 마친 뒤 reflect-and-apply를 적용한다.
허용된 가역적 로컬 지침·원장 수정만 실행하고,
개인정보·memory·외부 발송·공개·제출·유료 실행은 기존 권한을 따른다.
일회성 예외는 해당 작업에 보존하고 전역 기본값으로 확대하지 않는다.
```

분석만 요청했다면 파일을 수정하지 않습니다. 반대로 이미 허용된 로컬 수정이라면 같은 승인을 반복해서 요구하지 않습니다. 민감한 값의 저장 경로와 memory 정책은 각 환경의 별도 규칙을 따릅니다.

## 저장 위치의 역할

| 위치 | 넣을 내용 | 넣지 않을 내용 |
|---|---|---|
| `AGENTS.md` | 지속 기본값, 호출 조건, 조회 연결 | 상세 대화 일기, 민감한 확인값 |
| 소유 스킬/참조 | 선택·실행·검수의 반복 절차 | 무관한 개인 이력 전체 |
| 사실 원장 | 허용된 재사용 사실, 출처·확인일·증거 상태 | 확인되지 않은 성과·기간·숙련도 |
| 현재 작업 기록 | 이번 문서의 예외·제외, 당시 상태와 검증 | 다른 모든 작업에 대한 일괄 금지 |

특정 개인 원장이나 폴더를 요구하지 않습니다. 기존 환경에서 실제 사용하는 파일에 연결합니다.

## 예시: 이번 문서와 앞으로의 기준을 나누기

사용자: `이 제안서에는 장비 A가 안 맞아. 이 문서만 16pt로 하고, 다음부터 실제 업무 보고 골라줘.`

- 이번 제안서: 장비 A 대표 배치 제외, 16pt 유지.
- 앞으로의 선정 기준: 실제 업무의 행동·산출물과 후보의 수행 근거를 선정 전에 대조.
- 다른 문서: 기존 글꼴 기본값 유지. 장비 A가 실제 업무에 맞으면 다시 검토 가능.
- 자료 부족: 대체 사례를 만들지 않고 선정 보류와 필요한 자료만 기록.

반영 전후 파일과 검증 입력은 [전체 예시](references/worked-example.md)에서 확인할 수 있습니다.

## 패키지 구성

```text
reflect-and-apply/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── evidence-and-scope.md
│   ├── decision-guide.md
│   ├── change-procedure.md
│   ├── worked-example.md
│   └── acceptance-cases.md
├── scripts/validate_package.py
├── tests/test_validate_package.py
├── .github/workflows/validate.yml
├── requirements-dev.txt
├── README.md
└── LICENSE
```

## 검증

Python 3.10 이상에서 저장소 루트 기준으로 실행합니다.

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_package.py .
python -m unittest discover -s tests -v
```

`validate_package.py`는 읽기 전용입니다. 필수 파일, YAML 메타데이터, 본 패키지 형식의 상대 Markdown 파일 링크, 코드 펜스의 닫힘을 검사합니다. 웹 링크의 접속 여부·Markdown 앵커·참조형 링크·의미적 정확도·개인정보 전체를 검사하지 않습니다. GitHub Actions에서도 같은 검사를 실행합니다.

행동 검증은 별도입니다. [검증 사례](references/acceptance-cases.md)에는 범위·사실·권한·중복·동시 수정에 대한 20개 합성 입력과 통과/실패 기준이 있습니다. 각 변경에는 관련 실패 조건과 정상 예외를 골라 실제 관측을 남기세요. 사례 목록이 있다는 사실을 모두 통과했다는 결과로 해석하지 않습니다.

## 제한과 유지보수

- 모델을 재학습하거나 완전한 재발 방지·정확도·시간 절감을 보장하지 않습니다.
- 다른 채팅 읽기는 호스트가 제공하는 도구·접근 권한에 달려 있습니다. 도구가 없으면 현재 근거와 미확인 범위를 사용합니다.
- 백그라운드 감시·예약·외부 발송·공개·최종 제출·유료 실행을 설치하지 않습니다.
- 이 패키지의 예시는 합성입니다. 실제 대화·개인 원장·회사 보호자료를 포함하지 않습니다.
- 새 오류를 발견하면 같은 금지문을 계속 추가하기보다, 누락된 조회·선정·검수 단계부터 고칩니다.
- 업데이트 전에는 로컬 수정과 diff를 확인하세요. 설치 경로의 내용을 원격 버전으로 강제 덮어쓰지 마세요.

문제 제보에는 민감한 원문 대신 익명화한 최소 입력, 기대한 행동, 관측한 행동, 사용한 버전, 적용 범위와 권한을 적어 주세요.

## 출처와 라이선스

사용자가 보유한 기존 `reflect-and-apply` 지침을 바탕으로 공개 배포용 설명·조건별 참조·합성 예시·검증 자료를 확장했습니다. 작성과 검증에 Codex를 사용했습니다. 특정 개인의 실제 경력·확인값을 패키지의 기본값으로 포함하지 않았습니다.

스킬 형식·검색 위치·호출 설정은 [OpenAI 공식 스킬 문서](https://learn.chatgpt.com/docs/build-skills)를 참고했습니다. 문서의 긴 본문이나 다른 스킬의 구현을 복제하지 않았습니다. OpenAI의 공식 배포물·제휴·인증을 뜻하지 않습니다.

[MIT License](LICENSE).
