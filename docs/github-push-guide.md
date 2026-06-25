# 로컬 Git → GitHub 저장소 생성 및 Push 가이드

로컬 프로젝트를 GitHub에 올리는 전체 과정을 정리한 문서입니다.  
이 프로젝트(`MagicSquare_1004`)에 실제 적용했던 순서를 기준으로 작성했습니다.

---

## 사전 준비

| 항목 | 확인 방법 |
|------|-----------|
| Git 설치 | `git --version` |
| GitHub 계정 | https://github.com |
| GitHub CLI (선택) | `gh --version` |

GitHub CLI(`gh`)가 없어도 웹에서 저장소를 만든 뒤 push할 수 있습니다.  
아래 **방법 A**는 `gh` 사용, **방법 B**는 웹 UI 사용입니다.

---

## 1단계: 로컬 Git 상태 확인

프로젝트 폴더로 이동한 뒤 상태를 확인합니다.

```powershell
Set-Location "c:\DEV\MagicSquare_1004"
git status
```

확인할 내용:

- 브랜치 이름 (예: `main`)
- 커밋이 있는지 (`No commits yet` 이면 아직 없음)
- 추적되지 않은 파일 목록

원격 저장소가 연결되어 있는지 확인:

```powershell
git remote -v
```

아무것도 출력되지 않으면 원격이 아직 없는 상태입니다.

---

## 2단계: 초기 커밋 만들기

**커밋이 하나도 없으면 push할 수 없습니다.**  
올릴 파일을 스테이징하고 커밋합니다.

```powershell
git add .
git commit -m "Initial commit"
```

특정 파일만 올릴 경우:

```powershell
git add AGENTS.md
git commit -m "Initial commit"
```

커밋 이력 확인:

```powershell
git log --oneline
```

---

## 3단계: GitHub에 저장소 생성

### 방법 A — GitHub CLI (`gh`) 사용

GitHub에 로그인되어 있어야 합니다.

```powershell
gh auth status
```

로그인이 필요하면:

```powershell
gh auth login
```

저장소 생성 (이 프로젝트에서 사용한 명령):

```powershell
gh repo create MagicSquare_1004 --public --description "Magic Square project"
```

옵션 설명:

| 옵션 | 의미 |
|------|------|
| `MagicSquare_1004` | 저장소 이름 |
| `--public` | 공개 저장소 (비공개는 `--private`) |
| `--description` | 저장소 설명 |

한 번에 원격 추가 + push까지 하려면:

```powershell
gh repo create MagicSquare_1004 --public --description "Magic Square project" --source=. --remote=origin --push
```

> 이 명령을 쓰려면 **2단계(초기 커밋)** 가 먼저 완료되어 있어야 합니다.

### 방법 B — GitHub 웹에서 생성

1. https://github.com/new 접속
2. Repository name: `MagicSquare_1004`
3. Public / Private 선택
4. **"Add a README file" 등은 체크하지 않음** (로컬에 이미 파일이 있으므로)
5. **Create repository** 클릭

---

## 4단계: 원격 저장소 연결

`gh repo create`만 실행하고 push를 따로 하는 경우, 원격을 추가합니다.

```powershell
git remote add origin https://github.com/yoon2eyo/MagicSquare_1004.git
```

`yoon2eyo`는 본인 GitHub 사용자명으로 바꿉니다.

이미 `origin`이 있는데 URL을 바꿔야 할 때:

```powershell
git remote set-url origin https://github.com/<사용자명>/MagicSquare_1004.git
```

연결 확인:

```powershell
git remote -v
```

---

## 5단계: GitHub에 Push

```powershell
git push -u origin main
```

- `-u` : 이후 `git push`만 입력해도 `origin/main`을 추적
- `main` : 로컬 브랜치 이름 (다르면 해당 이름 사용)

성공 시 예시 출력:

```
To https://github.com/yoon2eyo/MagicSquare_1004.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

---

## 6단계: 결과 확인

로컬:

```powershell
git status
```

`Your branch is up to date with 'origin/main'.` 이 보이면 동기화 완료입니다.

브라우저:

https://github.com/yoon2eyo/MagicSquare_1004

---

## 이후 변경 사항 올리기

파일 수정 후 반복하는 일반 흐름:

```powershell
git add .
git commit -m "변경 내용 요약"
git push
```

---

## 문제 해결

### `fatal: your current branch 'main' does not have any commits yet`

→ **2단계** 초기 커밋을 먼저 만듭니다.

### `gh auth status` keyring 타임아웃

Windows에서 자격 증명 저장소(keyring) 접근이 지연될 때 발생할 수 있습니다.

```powershell
gh auth login
```

로 재인증 후 다시 시도합니다. `git push`는 별도 자격 증명으로 동작하는 경우가 많습니다.

### `gh repo create` GraphQL 타임아웃

네트워크 지연 시 발생할 수 있습니다. 잠시 후 저장소 생성 명령만 다시 실행하거나, **방법 B(웹 UI)** 로 저장소를 만든 뒤 4~5단계를 진행합니다.

### `remote origin already exists`

```powershell
git remote remove origin
git remote add origin https://github.com/<사용자명>/MagicSquare_1004.git
```

### push 시 인증 실패

- HTTPS: GitHub Personal Access Token 또는 `gh auth login`으로 인증
- SSH 사용 시 원격 URL을 `git@github.com:<사용자명>/MagicSquare_1004.git` 형식으로 설정

---

## 이 프로젝트 적용 요약

| 단계 | 실행 내용 |
|------|-----------|
| 1 | `git status` — `main` 브랜치, 커밋 없음, `AGENTS.md` 미추적 확인 |
| 2 | `git add AGENTS.md` → `git commit -m "Initial commit"` |
| 3 | `gh repo create MagicSquare_1004 --public --description "Magic Square project"` |
| 4 | `git remote add origin https://github.com/yoon2eyo/MagicSquare_1004.git` |
| 5 | `git push -u origin main` |

결과 저장소: https://github.com/yoon2eyo/MagicSquare_1004
