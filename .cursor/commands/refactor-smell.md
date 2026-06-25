---
description: REFACTOR 스멜 탐지 (수정 금지)
---

# /refactor-smell

Phase: **refactor** | Mode: Ask | **수정 금지**

## 전제
`pytest` 전체 **PASS** 상태

## 작업
코드에서 P0/P1/P2 우선순위로 스멜 1~3개 식별만 한다. 파일은 수정하지 않는다.

## 출력
| 우선순위 | 스멜 | 위치 | 제안 (REFACTOR-safe용) |

다음: `/refactor-safe`로 안전 정제
