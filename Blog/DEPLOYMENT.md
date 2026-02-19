# Django 블로그 프로젝트 배포 체크리스트

## 프로덕션 배포 전 필수 사항

### 1. 환경 변수 설정
- [ ] `.env` 파일 확인
  - `DEBUG=False` 설정
  - `SECRET_KEY`를 안전한 랜덤 문자열로 변경
  - `ALLOWED_HOSTS`에 도메인 추가 (예: `example.com,www.example.com`)

### 2. 데이터베이스 설정
- [ ] SQLite에서 PostgreSQL로 변경 (권장)
- [ ] 데이터베이스 백업 전략 수립
- [ ] 마이그레이션 실행 확인

### 3. 정적 파일
- [ ] `python manage.py collectstatic` 실행
- [ ] STATIC_ROOT 경로 확인
- [ ] Nginx에서 정적 파일 서빙 설정

###4. 보안 설정
- [ ] `config/settings.py`에서 다음 설정 활성화:
  ```python
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  SECURE_BROWSER_XSS_FILTER = True
  SECURE_CONTENT_TYPE_NOSNIFF = True
  X_FRAME_OPTIONS = 'DENY'
  ```
- [ ] HTTPS 인증서 설정 (Let's Encrypt 권장)

### 5. 서버 설정
- [ ] Gunicorn 설치 및 설정
  ```bash
  pip install gunicorn
  gunicorn config.wsgi:application --bind 0.0.0.0:8000
  ```
- [ ] Nginx 리버스 프록시 설정
- [ ] 서비스 자동 시작 설정 (systemd)

### 6. 성능 최적화
- [ ] 데이터베이스 커넥션 풀링 설정
- [ ] 캐싱 설정 (Redis/Memcached)
- [ ] 압축 활성화 (Gzip)

### 7. 모니터링
- [ ] 로그 설정 및 수집
- [ ] 에러 추적 (Sentry 등)
- [ ] 서버 모니터링 설정

### 8. 최종 확인
- [ ] 모든 URL 접근 테스트
- [ ] 사용자 플로우 테스트 (회원가입 → 로그인 → 글 작성 → 수정 → 삭제)
- [ ] 권한 검증 확인
- [ ] 모바일 반응형 확인
- [ ] 브라우저 호환성 테스트

## 배포 예시 (Ubuntu + Nginx + Gunicorn)

### 1. 서버 패키지 설치
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

### 2. 프로젝트 배포
```bash
cd /var/www
git clone <repository-url>
cd Blog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 데이터베이스 설정
```bash
sudo -u postgres createdb blogdb
sudo -u postgres createuser bloguser -P
```

### 4. Gunicorn 서비스 설정
`/etc/systemd/system/blog.service`:
```ini
[Unit]
Description=Django Blog Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/Blog
Environment="PATH=/var/www/Blog/venv/bin"
ExecStart=/var/www/Blog/venv/bin/gunicorn --workers 3 --bind unix:/var/www/Blog/blog.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 5. Nginx 설정
`/etc/nginx/sites-available/blog`:
```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/Blog;
    }

    location /media/ {
        root /var/www/Blog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Blog/blog.sock;
    }
}
```

### 6. 서비스 시작
```bash
sudo systemctl start blog
sudo systemctl enable blog
sudo systemctl restart nginx
```

## 롤백 계획

문제 발생 시 롤백 절차:
1. 이전 버전으로 코드 롤백 (`git checkout <previous-commit>`)
2. 데이터베이스 백업 복원
3. 서비스 재시작 (`sudo systemctl restart blog`)
4. 캐시 클리어

## 참고 자료

- [Django 배포 가이드](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Nginx 설정 가이드](https://nginx.org/en/docs/)
- [Gunicorn 문서](https://docs.gunicorn.org/)
