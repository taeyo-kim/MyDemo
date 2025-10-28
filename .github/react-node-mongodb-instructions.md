# React, Node.js, MongoDB 프로젝트 개발 지침

## 프로젝트 개요

이 프로젝트는 React와 Node.js를 사용한 풀스택 웹 애플리케이션으로, 데이터 저장소로 MongoDB를 활용합니다. 사용자 친화적인 인터페이스와 효율적인 데이터 처리를 목표로 합니다.

## 아키텍처

- **프론트엔드**: React 18, React Router v6, Redux Toolkit을 사용한 SPA 구조
- **백엔드**: Node.js 18+, Express 4.x를 사용한 RESTful API
- **데이터베이스**: MongoDB Atlas, Mongoose ODM
- **인증**: JWT 기반 사용자 인증 시스템
- **배포**: Docker 컨테이너화, GitHub Actions를 통한 CI/CD

## 폴더 구조

```
/
├── client/                # 프론트엔드 (React)
│   ├── public/            # 정적 파일
│   ├── src/               # 소스 코드
│   │   ├── assets/        # 이미지, 폰트 등 자산
│   │   ├── components/    # 재사용 가능한 컴포넌트
│   │   │   ├── common/    # 공통 컴포넌트
│   │   │   └── layout/    # 레이아웃 관련 컴포넌트
│   │   ├── context/       # React Context
│   │   ├── hooks/         # 커스텀 React hooks
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── redux/         # Redux 상태 관리
│   │   │   ├── slices/    # Redux Toolkit slices
│   │   │   └── store.js   # Redux store 설정
│   │   ├── services/      # API 호출 서비스
│   │   ├── utils/         # 유틸리티 함수
│   │   ├── App.js         # 메인 App 컴포넌트
│   │   └── index.js       # 진입점
│   └── package.json       # 프론트엔드 의존성
│
├── server/                # 백엔드 (Node.js/Express)
│   ├── config/            # 환경 설정
│   ├── controllers/       # 요청 핸들러
│   ├── middleware/        # 미들웨어
│   ├── models/            # Mongoose 모델
│   ├── routes/            # API 라우트
│   ├── services/          # 비즈니스 로직
│   ├── utils/             # 유틸리티 함수
│   ├── app.js             # Express 앱 설정
│   ├── server.js          # 서버 진입점
│   └── package.json       # 백엔드 의존성
│
├── .env.example           # 환경 변수 예시
├── docker-compose.yml     # Docker Compose 설정
└── README.md              # 프로젝트 문서
```

## 기술 스택 및 라이브러리

### 프론트엔드
- **핵심**: React 18, React Router, Redux Toolkit
- **UI**: Material-UI v5 또는 Tailwind CSS v3.x
- **폼 관리**: React Hook Form, Yup(유효성 검사)
- **API 통신**: Axios
- **상태 관리**: Redux Toolkit, React Query
- **유틸리티**: date-fns, lodash
- **테스팅**: Jest, React Testing Library

### 백엔드
- **핵심**: Node.js, Express
- **데이터베이스**: MongoDB, Mongoose
- **인증/인가**: JWT, Passport.js
- **유효성 검사**: Joi 또는 express-validator
- **로깅**: Winston, Morgan
- **보안**: Helmet, CORS, rate-limiting
- **테스팅**: Mocha, Chai, Supertest

## 코딩 표준

### 공통 규칙
- ESLint와 Prettier를 사용하여 코드 스타일 통일
- 명시적인 타입 체크를 위해 PropTypes 또는 TypeScript 사용
- Git commit 메시지는 conventional commits 형식 준수
- 모든 API 엔드포인트는 문서화 (Swagger/OpenAPI)

### JavaScript/React 규칙
- 문장 끝에 세미콜론 사용
- 문자열은 작은따옴표(`'`) 사용
- 들여쓰기는 2칸 공백
- 함수형 컴포넌트와 React Hooks 사용
- 컴포넌트 이름은 PascalCase, 일반 함수와 변수는 camelCase
- Props 구조 분해 할당 사용
- 컴포넌트 내 함수는 useCallback으로 메모이제이션
- 불변성 유지를 위해 스프레드 연산자 및 불변 업데이트 패턴 사용

### Node.js/Express 규칙
- 비동기 작업에는 async/await 사용
- 에러 처리는 try/catch 또는 Promise.catch() 사용
- 라우트 핸들러는 controller 함수로 분리
- 데이터 접근 로직은 service 계층으로 분리
- 환경 변수를 통한 설정 관리 (.env)
- HTTP 상태 코드 적절하게 사용

## MongoDB 모델링 가이드라인
- 스키마는 Mongoose를 통해 정의, 필드 유효성 검사 포함
- 관계는 참조(reference) 방식 선호, 필요한 경우 내장(embedding) 사용
- 인덱스는 자주 조회되는 필드에 적용
- 가상 필드(virtual)와 미들웨어(pre/post hooks) 적절히 활용
- 트랜잭션이 필요한 작업은 세션 사용

## API 설계 원칙
- RESTful 원칙 준수 (적절한 HTTP 메소드 사용)
- 일관된 엔드포인트 네이밍: `/api/v1/resources`
- 응답은 항상 JSON 형식으로 통일
- 페이지네이션, 필터링, 정렬 기능 지원
- 에러 응답은 표준 포맷 유지: `{ status, message, errors? }`
- API 버전 관리 통해 하위 호환성 유지

## 보안 가이드라인
- 민감한 정보는 환경 변수로 관리
- API 요청에 대한 유효성 검사 철저히 수행
- CORS 설정 명확히 지정
- 비밀번호 해싱(bcrypt) 필수
- JWT 토큰 관리와 갱신 전략 수립
- XSS, CSRF, SQL 인젝션 방어 대책 구현

## 성능 최적화
- 프론트엔드: React.memo, useMemo, lazy loading 활용
- 백엔드: 캐싱 전략, 데이터베이스 쿼리 최적화
- 이미지 최적화 및 CDN 사용 권장
- 번들 사이즈 최소화 (code splitting)

## UI/UX 가이드라인
- 반응형 디자인으로 모바일 친화적 UI 구현
- 접근성(a11y) 표준 준수
- 다크 모드 지원
- 로딩 상태와 에러 상태 명확히 표시
- 사용자 피드백 및 알림 시스템 구현

## 테스팅 전략
- 단위 테스트: 핵심 유틸리티 및 비즈니스 로직
- 통합 테스트: API 엔드포인트, 데이터베이스 상호작용
- E2E 테스트: 주요 사용자 플로우
- 테스트 커버리지 70% 이상 유지

## MongoDB 연결 및 데이터 모델링 예시

### 연결 설정 (server/config/database.js)
```javascript
const mongoose = require('mongoose');
require('dotenv').config();

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('MongoDB 연결 성공');
  } catch (error) {
    console.error('MongoDB 연결 실패:', error.message);
    process.exit(1);
  }
};

module.exports = connectDB;
```

### 사용자 모델 예시 (server/models/User.js)
```javascript
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: [true, '사용자명은 필수입니다'],
    unique: true,
    trim: true,
    minlength: [3, '사용자명은 최소 3자 이상이어야 합니다'],
  },
  email: {
    type: String,
    required: [true, '이메일은 필수입니다'],
    unique: true,
    match: [
      /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
      '유효한 이메일 주소를 입력해주세요',
    ],
  },
  password: {
    type: String,
    required: [true, '비밀번호는 필수입니다'],
    minlength: [6, '비밀번호는 최소 6자 이상이어야 합니다'],
    select: false,
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user',
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

// 비밀번호 해싱 미들웨어
UserSchema.pre('save', async function (next) {
  if (!this.isModified('password')) {
    return next();
  }
  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

// 비밀번호 검증 메서드
UserSchema.methods.matchPassword = async function (enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password);
};

module.exports = mongoose.model('User', UserSchema);
```

## React 컴포넌트 작성 가이드

### 기본 컴포넌트 구조 (client/src/components/common/Button.js)
```jsx
import React from 'react';
import PropTypes from 'prop-types';

const Button = ({ 
  text, 
  type = 'button', 
  variant = 'primary', 
  onClick, 
  disabled = false 
}) => {
  const baseClasses = 'px-4 py-2 rounded font-medium transition-colors';
  
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  };
  
  return (
    <button
      type={type}
      className={`${baseClasses} ${variantClasses[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      onClick={onClick}
      disabled={disabled}
    >
      {text}
    </button>
  );
};

Button.propTypes = {
  text: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger']),
  onClick: PropTypes.func,
  disabled: PropTypes.bool,
};

export default Button;
```

### API 서비스 예시 (client/src/services/api.js)
```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 - 토큰 추가
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 응답 인터셉터 - 토큰 만료 처리
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // 토큰 만료 처리 로직
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```