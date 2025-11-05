# Django 메모장 웹 애플리케이션

Django 기반의 간단한 메모장 웹 애플리케이션입니다.

## 주요 기능
- 사용자 로그인 및 회원가입
- 메모 작성, 수정, 삭제
- 메모 목록 조회

## 기술 스택
- Backend: Django
- Database: SQLite
- Frontend: Django Templates + Bootstrap
- Authentication: Django 내장 인증 시스템

## 설치 및 실행

### 1. 가상환경 생성 및 활성화
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. 패키지 설치
```powershell
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가합니다:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. 데이터베이스 마이그레이션
```powershell
python manage.py migrate
```

### 5. 개발 서버 실행
```powershell
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 접속

## 프로젝트 구조
```
memojang/
├── apps/
│   ├── memos/          # 메모 앱
│   └── users/          # 사용자 앱
├── db/                 # 데이터베이스
├── static/             # 정적 파일
│   ├── css/
│   └── js/
├── templates/          # 템플릿
│   ├── base.html
│   ├── home.html
│   ├── memos/
│   └── users/
├── memojang/           # 메인 프로젝트 설정
└── manage.py
```

## 개발 중
이 프로젝트는 현재 개발 중입니다.
