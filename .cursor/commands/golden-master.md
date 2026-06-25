---
description: Golden Master 회귀 안전망 연결
---

# /golden-master

Phase: **green** · GM | GREEN PASS 이후에만 실행

## 순서 (엄수)
1. GREEN PASS 확인
2. `tests/_approval.py` + `tests/golden/<id>_approved.txt` 연결
3. 기준 생성: `$env:UPDATE_GOLDEN=1; pytest <test_path> -v`
4. 검증: `pytest <test_path> -v` (환경변수 없이)

## 참고 파일 형식
```
2,3
4,4
# 1-index row, col
# row-major (I6)
```

연결 없이 `UPDATE_GOLDEN=1`만 실행하면 무시된다.
