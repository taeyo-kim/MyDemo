---
description: REST API 보안 검사 가이드라인
applyTo: '**'
---

## REST API 보안 검사 항목

### 인증 & 권한
- **강력한 인증**: OAuth 2.0, JWT, API Keys 사용
- **토큰 관리**: Access Token 만료(15-60분), Refresh Token 갱신
- **권한 검증**: 리소스 소유권 확인, 수평/수직 권한 상승 방지
- **최소 권한 원칙**: 필요한 최소한의 권한만 부여

### 데이터 보안
- **HTTPS 필수**: TLS 1.2 이상, HSTS 헤더 설정
- **입력 검증**: 모든 입력 데이터 유효성 검사, 화이트리스트 방식
- **민감 데이터**: 비밀번호 해싱(bcrypt/Argon2), 개인정보 암호화
- **응답 필터링**: 민감 정보(비밀번호, 토큰) 응답에서 제외

### Injection 방지
- **파라미터화된 쿼리**: ORM 또는 Prepared Statements 사용
- **NoSQL Injection**: 사용자 입력을 직접 쿼리에 삽입 금지

### Rate Limiting
- **속도 제한**: IP/사용자별 rate limiting 구현
- **429 응답**: Too Many Requests + Retry-After 헤더

### 보안 헤더
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'