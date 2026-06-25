# Project 개요
4×4 마방진

# 작업 방식
## C2C · Dual-Track · ARRR
ECB 방향: Entity는 Boundary/Control를 import하지 않는다 (순수 로직만).
### C2C
PRD → To-Do → Test Case → 구현 연결고리를 끊지 않는 추적성
### Dual-Track(ECB)
Track A(UI/Boundary) + Track B(Domain/Logic)
### ARRR
Ask(RED)→Respond(GREEN)→Refine(REFACTOR)→Repeat

# Branch 전략
브랜치 전략 — 단계가 곧 브랜치
ARRR의 각 단계를 브랜치로 분리하여, '어느 단계에서 무엇이 바뀌었나'가 이력만으로 추적

```
git checkout -b staging # main 에서 시작
git checkout -b spec # 세션 3 — 설계·계약
git checkout -b red # 세션 4 — A=Ask(RED)
git checkout -b green # R=Respond(GREEN) → refactoring → new_features
```
