---
applyTo: "**/*.py"
---

# Python Instructions

## Coding Style
- **PEP 8** 준수, 함수/변수는 **snake_case**
- 모든 공개 함수에 **type hints**와 **docstring** 필수
- 파일/모듈당 **단일 책임** 지향

## Packaging & Env
- 패키지 관리: **`uv` 또는 `pip` + `requirements.txt`/`pyproject.toml`**
- 런타임 설정값은 **환경변수** 또는 설정파일로 주입(하드코딩 금지)

## Error Handling
- 구체적인 예외 타입 사용, **try/except** 범위 최소화
- 외부 I/O에는 **타임아웃**과 **재시도**(예: tenacity) 권장

## Testing (applyTo: tests/**)
- **pytest** + **coverage** ≥ 85%
- **arrange/act/assert** 주석을 통해 단계 명시
- **fixtures**로 공통 준비 로직 재사용

## Performance & Data
- 대용량 데이터에는 **generators**/**lazy evaluation** 활용
- **pandas** 사용 시, 연산은 **벡터화** 우선

## Security
- 비밀값은 환경변수/Key Vault 등에서 로드
- 외부 입력은 **검증 및 sanitize** 수행