# Django 블로그 프로젝트

Django 프레임워크 기반의 간단한 블로그 웹 애플리케이션입니다.

## 주요 기능

- 사용자 인증 (로그인, 회원가입, 로그아웃)
- 블로그 포스트 CRUD (생성, 조회, 수정, 삭제)
- 포스트 목록 및 상세보기
- 페이지네이션
- 권한 관리 (작성자만 수정/삭제 가능)
- 관리자 인터페이스

## 기술 스택

- **Backend**: Django 5.2.8
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Database**: SQLite
- **Authentication**: Django 내장 인증 시스템
- **환경 변수 관리**: python-dotenv

## 설치 및 실행

### 1. 가상환경 설정

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. 의존성 설치

```powershell
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가합니다:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. 데이터베이스 마이그레이션

```powershell
python manage.py migrate
```

### 5. 슈퍼유저 생성 (관리자 계정)

```powershell
python manage.py createsuperuser
```

프롬프트에 따라 사용자명, 이메일, 비밀번호를 입력합니다.

### 6. 개발 서버 실행

```powershell
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 으로 접속합니다.

### 7. 관리자 페이지 접속

`http://127.0.0.1:8000/admin/` 으로 접속하여 슈퍼유저 계정으로 로그인합니다.

## 프로젝트 구조

```
Blog/
├── apps/                   # Django 앱
│   ├── posts/              # 블로그 포스트 앱
│   └── users/              # 사용자 관리 앱
├── blogApp/                # 메인 프로젝트 설정
├── db/                     # 데이터베이스 파일
├── static/                 # 정적 파일
│   ├── css/
│   └── js/
├── templates/              # 템플릿
│   ├── posts/
│   └── users/
├── manage.py
└── requirements.txt
```

## 사용 방법

### 회원가입 및 로그인

1. 홈페이지에서 "회원가입" 클릭
2. 사용자명, 이메일, 비밀번호 입력
3. 로그인하여 블로그 이용

### 포스트 작성

1. 로그인 후 "새 포스트" 클릭
2. 제목과 내용 입력
3. "작성" 버튼 클릭

### 포스트 수정/삭제

1. 본인이 작성한 포스트 상세 페이지에서 "수정" 또는 "삭제" 버튼 클릭
2. 수정 시 내용 변경 후 저장
3. 삭제 시 확인 후 삭제

## 보안 기능

- CSRF 보호
- XSS 방지
- 세션 쿠키 보안
- 비밀번호 해싱
- 권한 기반 접근 제어
- HTTPS 설정 (프로덕션)

## 개발자

- Tae young Kim

## 라이센스

MIT License
