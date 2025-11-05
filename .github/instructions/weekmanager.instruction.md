# WeekManager 개발 지침서

## 요구사항
주간 일정 관리 웹 애플리케이션 (오늘 기준 7일 표시, 오전7시~오후7시, 드래그앤드롭 일정 이동, 회원가입/로그인, SQLite 저장)

## 기술 스택
- **프론트엔드**: React + TypeScript, Vite, Tailwind CSS
- **백엔드**: Node.js + TypeScript, Express
- **데이터베이스**: SQLite (better-sqlite3)
- **인증**: JWT + bcrypt
- **드래그앤드롭**: dnd-kit

## 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  display_name TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### events 테이블
```sql
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  body TEXT,
  start_iso TEXT NOT NULL,
  end_iso TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## REST API

### 인증
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/me` - 현재 사용자 정보

### 일정 관리
- `GET /api/events?start=YYYY-MM-DD&end=YYYY-MM-DD` - 주간 일정 조회
- `POST /api/events` - 일정 생성
- `PUT /api/events/:id` - 일정 수정
- `DELETE /api/events/:id` - 일정 삭제

## 핵심 검증 규칙
- 시작시간 < 종료시간
- 07:00 ≤ 시간 ≤ 19:00
- 사용자는 자신의 일정만 CRUD 가능

## 프로젝트 구조
```
/client
  /src
    /components (WeekView, DayColumn, EventBlock, EventModal)
    /hooks
    /services
/server
  /src
    app.ts
    /routes
    /controllers
    /db
/db
  app.db
```

## 개발 시작
```powershell
# 서버
cd server
npm install
npm run dev

# 클라이언트
cd client  
npm install
npm run dev
```

## 핵심 기능
1. **WeekView**: 오늘 기준 7일 표시 (07:00-19:00 그리드)
2. **EventBlock**: 일정을 네모 블록으로 표시, 드래그 가능
3. **드래그앤드롭**: 같은 주 내에서 요일 이동, 서버 동기화
4. **인증**: JWT 기반 사용자별 일정 관리
5. **시간 검증**: 서버에서 시간 범위 강제 검증