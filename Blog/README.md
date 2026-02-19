# Django 블로그 프로젝트

Django 기반의 간단한 블로그 웹 애플리케이션입니다. 사용자 인증, 블로그 글 CRUD, 조회수 추적, 정렬 기능을 포함합니다.

## 주요 기능

### 사용자 인증
- 회원가입
- 로그인 / 로그아웃
- Django 내장 인증 시스템 활용

### 블로그 기능
- 블로그 글 작성 (로그인 필수)
- 블로그 글 목록 조회 (날짜순/조회수순 정렬)
- 블로그 글 상세 조회 (조회수 자동 증가)
- 블로그 글 수정 (작성자만 가능)
- 블로그 글 삭제 (작성자만 가능)
- 페이지네이션 (10개씩)

## 기술 스택

- **Backend**: Django 4.2
- **Frontend**: TailwindCSS (CDN)
- **Database**: SQLite (개발), PostgreSQL (프로덕션 권장)
- **Python**: 3.8+

## 프로젝트 구조

```
Blog/
├── apps/
│   ├── posts/          # 블로그 글 앱
│   │   ├── models.py   # Post 모델
│   │   ├── views.py    # CRUD 뷰
│   │   ├── forms.py    # PostForm
│   │   ├── urls.py     # URL 패턴
│   │   ├── admin.py    # Admin 설정
│   │   └── tests.py    # 테스트
│   │
│   └── users/          # 사용자 인증 앱
│       ├── views.py    # 인증 뷰
│       ├── forms.py    # SignUpForm
│       ├── urls.py     # URL 패턴
│       └── tests.py    # 테스트
│
├── config/             # Django 설정
│   ├── settings.py     # 프로젝트 설정
│   ├── urls.py         # 루트 URL 설정
│   └── wsgi.py         # WSGI 설정
│
├── templates/          # Django 템플릿
│   ├── base.html       # 기본 레이아웃
│   ├── users/          # 인증 템플릿
│   └── posts/          # 블로그 템플릿
│
├── static/             # 정적 파일
│   ├── css/            # CSS 파일
│   └── js/             # JavaScript 파일
│
├── .env                # 환경 변수 (git ignored)
├── .env.example        # 환경 변수 예제
├── requirements.txt    # Python 패키지 목록
└── manage.py           # Django 관리 스크립트
```

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd MyDemo/Blog
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고, 필요한 값들을 설정합니다:

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 슈퍼유저 생성

```bash
python manage.py createsuperuser
```

프롬프트에 따라 사용자명, 이메일, 비밀번호를 입력합니다.

### 7. 개발 서버 실행

```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/`로 접속합니다.

## 사용 방법

### 관리자 페이지 접근

`http://127.0.0.1:8000/admin/`에서 슈퍼유저로 로그인하여 Post 모델을 관리할 수 있습니다.

### 블로그 사용

1. **회원가입**: `/users/signup/`에서 계정 생성
2. **로그인**: `/users/login/`에서 로그인
3. **글 작성**: 로그인 후 네비게이션 바의 "글 작성" 버튼 클릭
4. **글 목록**: `/posts/`에서 모든 글 목록 확인
5. **정렬**: "최신순" 또는 "조회수순" 버튼으로 정렬
6. **글 상세**: 글 제목 클릭으로 상세 페이지 이동 (조회수 자동 증가)
7. **글 수정/삭제**: 자신이 작성한 글의 상세 페이지에서 "수정" 또는 "삭제" 버튼 클릭

## 테스트 실행

```bash
python manage.py test
```

총 19개의 테스트가 포함되어 있습니다:
- Post 모델 테스트
- 블로그 CRUD 뷰 테스트
- 권한 검증 테스트
- 인증 플로우 테스트

## 배포 준비

### 프로덕션 설정 체크리스트

1. **환경 변수 설정**
   - `DEBUG=False`
   - `SECRET_KEY`를 안전한 랜덤 문자열로 변경
   - `ALLOWED_HOSTS`에 도메인 추가

2. **정적 파일 수집**
   ```bash
   python manage.py collectstatic
   ```

3. **데이터베이스**
   - SQLite 대신 PostgreSQL 사용 권장
   - `config/settings.py`의 `DATABASES` 설정 변경

4. **HTTPS 설정**
   - `SECURE_SSL_REDIRECT = True`
   - `SESSION_COOKIE_SECURE = True`
   - `CSRF_COOKIE_SECURE = True`

5. **서버 설정**
   - Gunicorn + Nginx 권장
   - 예: `gunicorn config.wsgi:application --bind 0.0.0.0:8000`

## 개발 가이드

### 새로운 기능 추가

1. 필요한 모델 변경: `apps/posts/models.py` 수정
2. 마이그레이션 생성: `python manage.py makemigrations`
3. 마이그레이션 적용: `python manage.py migrate`
4. 뷰/폼 구현
5. URL 패턴 추가
6. 템플릿 작성
7. 테스트 작성 및 실행

### 코드 스타일

- PEP 8 준수
- Class-Based Views 우선 사용
- 권한 제어는 Mixin 패턴 사용 (`LoginRequiredMixin`, `UserPassesTestMixin`)

## 라이선스

이 프로젝트는 학습 목적으로 작성되었습니다.

## 문의

문제가 발생하거나 질문이 있으면 GitHub Issues를 통해 문의해주세요.
