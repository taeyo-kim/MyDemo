# Django 블로그 프로젝트

Django 기반의 블로그 웹 애플리케이션입니다.

## 주요 기능
- 사용자 로그인 및 회원가입
- 블로그 글 작성, 수정, 삭제
- 블로그 글 목록 조회
- 작성자 권한 검증

## 기술 스택
- **Backend**: Django 4.2
- **Frontend**: Django Templates + TailwindCSS
- **Database**: SQLite (개발용)
- **Authentication**: Django 내장 인증 시스템

## 설치 및 실행

### 1. 저장소 클론
```powershell
git clone <repository-url>
cd MyDemo-Copilot/Blog
```

### 2. 가상환경 생성 및 활성화
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. 패키지 설치
```powershell
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일에서 `SECRET_KEY`를 안전한 값으로 변경하세요.

### 5. 데이터베이스 마이그레이션
```powershell
python manage.py migrate
```

### 6. 슈퍼유저 생성 (선택)
```powershell
python manage.py createsuperuser
```

### 7. 개발 서버 실행
```powershell
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 접속

## 프로젝트 구조
```
Blog/
├── apps/
│   ├── blog/          # 블로그 앱 (Post 모델, 뷰)
│   └── users/         # 사용자 앱 (인증)
├── config/            # Django 설정
├── db/                # 데이터베이스 파일
├── static/            # 정적 파일
├── templates/         # HTML 템플릿
│   ├── base.html
│   ├── home.html
│   ├── blog/
│   └── users/
├── manage.py
└── requirements.txt
```

## 주요 URL
- `/`: 홈페이지
- `/blog/`: 글 목록
- `/blog/<id>/`: 글 상세
- `/blog/new/`: 글 작성 (로그인 필수)
- `/blog/<id>/edit/`: 글 수정 (작성자만)
- `/blog/<id>/delete/`: 글 삭제 (작성자만)
- `/users/login/`: 로그인
- `/users/register/`: 회원가입
- `/admin/`: 관리자 페이지

## 보안 사항
- SECRET_KEY는 환경 변수로 관리 (`.env`)
- CSRF 보호 활성화
- 로그인 필수 기능에 LoginRequiredMixin 적용
- 작성자 권한 검증 (UserPassesTestMixin)

## 참고 문서
- [blog.instructions.md](../.github/instructions/blog.instructions.md)
- [Django 공식 문서](https://docs.djangoproject.com/)

## 개발 관련 GitHub Issues
- [#2 - STEP 1: 프로젝트 기반 설정](https://github.com/taeyo-kim/MyDemo-Copilot/issues/2)
- [#3 - STEP 2: Django 프로젝트 및 디렉토리 구조 생성](https://github.com/taeyo-kim/MyDemo-Copilot/issues/3)
- [#1 - STEP 3: Django 앱 및 모델 구현](https://github.com/taeyo-kim/MyDemo-Copilot/issues/1)
- [#4 - STEP 4: URL 라우팅 및 뷰 로직 구현](https://github.com/taeyo-kim/MyDemo-Copilot/issues/4)
- [#5 - STEP 5: 템플릿 및 TailwindCSS UI 구현](https://github.com/taeyo-kim/MyDemo-Copilot/issues/5)
- [#6 - STEP 6: 보안 설정 및 최종 검증](https://github.com/taeyo-kim/MyDemo-Copilot/issues/6)
