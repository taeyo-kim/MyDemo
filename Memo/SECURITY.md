# 보안 체크리스트

## 입력값 검증
- [x] 모든 폼에 Django Form 클래스 활용
- [x] 서버 사이드 유효성 검사 구현
- [x] SQL Injection 방지 (Django ORM 사용)
- [x] XSS 방지 (템플릿 자동 이스케이프)
- [x] CSRF 토큰 모든 POST 폼에 포함

## 인증 및 인가
- [x] LoginRequiredMixin으로 로그인 필수 뷰 보호
- [x] UserPassesTestMixin으로 작성자 권한 검증
- [x] 타인의 메모 접근 차단
- [x] URL 직접 접근 시도 차단

## 시크릿 관리
- [x] SECRET_KEY를 .env 파일로 분리
- [x] .gitignore에 .env 추가
- [x] python-decouple로 환경 변수 로드
- [x] DEBUG 설정 환경 변수화

## HTTPS 및 쿠키 보안
- [x] SECURE_SSL_REDIRECT (프로덕션)
- [x] SESSION_COOKIE_SECURE (프로덕션)
- [x] CSRF_COOKIE_SECURE (프로덕션)
- [x] SESSION_COOKIE_HTTPONLY
- [x] CSRF_COOKIE_HTTPONLY
- [x] SESSION_COOKIE_SAMESITE = 'Strict'
- [x] CSRF_COOKIE_SAMESITE = 'Strict'

## 비밀번호 정책
- [x] 최소 길이 8자
- [x] 사용자 속성 유사성 검사
- [x] 일반적인 비밀번호 차단
- [x] 숫자로만 구성된 비밀번호 차단

## 추가 보안 설정
- [x] SECURE_BROWSER_XSS_FILTER
- [x] SECURE_CONTENT_TYPE_NOSNIFF
- [x] X_FRAME_OPTIONS = 'DENY'
- [x] SECURE_HSTS_SECONDS (프로덕션)
- [x] SESSION_COOKIE_AGE (세션 타임아웃)

## 쿼리 최적화
- [x] select_related로 N+1 쿼리 방지
- [x] 인덱스 설정 (created_at, author)

## 보안 테스트 권장 사항
1. OWASP Top 10 취약점 점검
2. 침투 테스트 수행
3. 정기적인 의존성 업데이트
4. 로그 모니터링
5. Rate Limiting 구현 고려
6. 2단계 인증 추가 고려 (선택)

## 프로덕션 배포 전 체크리스트
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS 설정
- [ ] 정적 파일 수집 (collectstatic)
- [ ] 데이터베이스 백업 설정
- [ ] HTTPS 인증서 설치
- [ ] 방화벽 설정
- [ ] 로그 모니터링 설정
- [ ] 정기 백업 스케줄
