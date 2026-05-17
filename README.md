# 🎱 6/45 로또 웹 서비스

Django와 Docker를 사용하여 구현한 6/45 온라인 로또 서비스입니다.

---

## 📌 주요 기능

### 일반 사용자
- 회원가입 / 로그인 / 로그아웃
- 복권 구매 (수동 번호 선택 / 자동 번호 생성)
- 내 티켓 목록 및 당첨 결과 확인

### 관리자
- 회차별 판매 내역 조회
- 당첨 번호 추첨 실행
- 등수별 당첨 내역 확인

---

## 🛠 기술 스택

| 분류 | 기술 |
|---|---|
| Backend | Python 3.13, Django 6.0.5 |
| Database | PostgreSQL 15 |
| Web Server | Nginx (reverse proxy) |
| WAS | Gunicorn |
| Container | Docker, Docker Compose |

---

## 🏗 아키텍처

```
클라이언트
    ↓
Nginx (port 80)        ← 리버스 프록시 / 정적 파일 서빙
    ↓
Gunicorn (port 8000)   ← WSGI 서버
    ↓
Django App             ← 비즈니스 로직
    ↓
PostgreSQL (port 5432) ← 데이터베이스
```

### Docker 컨테이너 구성

```
lotto-web/
├── web      (python:3.13-slim)   Django + Gunicorn
├── db       (postgres:15)        PostgreSQL
└── nginx    (nginx:alpine)       리버스 프록시
```

---

## 📁 프로젝트 구조

```
Lotto-web/
├── config/                  # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # 회원가입/로그인
│   ├── views.py
│   └── urls.py
├── lottery/                 # 복권 핵심 로직
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   └── urls.py
├── admin_panel/             # 관리자 기능
│   ├── views.py
│   └── urls.py
├── templates/               # HTML 템플릿
│   ├── base.html
│   ├── accounts/
│   ├── lottery/
│   └── admin_panel/
├── docker/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── nginx/
│       └── nginx.conf
├── docker-compose.yml
├── requirements.txt
└── .env                     # 환경변수 (Git 제외)
```

---

## ⚙️ 데이터베이스 설계

| 모델 | 설명 |
|---|---|
| `Round` | 추첨 회차 (회차 번호, 추첨 여부) |
| `Ticket` | 구매한 복권 (사용자, 회차, 번호 6개, 자동여부) |
| `WinResult` | 당첨 번호 (당첨번호 6개, 보너스 번호) |
| `Prize` | 당첨 결과 (등수, 상금) |

---

## 🚀 실행 방법

### 사전 준비
- Docker Desktop 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/username/Lotto-web.git
cd Lotto-web
```

### 2. 환경변수 설정
`.env` 파일을 프로젝트 루트에 생성:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
POSTGRES_DB=lottodb
POSTGRES_USER=lottouser
POSTGRES_PASSWORD=your-password
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. 컨테이너 빌드 및 실행
```bash
docker-compose up --build
```

### 4. 관리자 계정 생성
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. 초기 회차 데이터 생성
```bash
docker-compose exec web python manage.py shell -c \
  "from lottery.models import Round; Round.objects.create(round_number=1)"
```

### 6. 접속
```
http://localhost
```

---

## 📋 주요 URL

| URL | 설명 |
|---|---|
| `/` | 로그인 페이지로 이동 |
| `/accounts/register/` | 회원가입 |
| `/accounts/login/` | 로그인 |
| `/lottery/buy/` | 복권 구매 |
| `/lottery/my-tickets/` | 내 티켓 목록 |
| `/admin-panel/draw/` | 추첨 실행 (관리자) |
| `/admin-panel/sales/` | 판매 내역 (관리자) |
| `/admin-panel/winners/` | 당첨 내역 (관리자) |

---

## 🤖 AI 도구 활용

본 프로젝트는 **Claude Sonnet 4.6 (Anthropic)** 를 활용하여 개발하였습니다.

| 활용 분야 | 내용 |
|---|---|
| 시스템 설계 | 멀티 컨테이너 아키텍처 구성 자문 |
| Docker 설정 | Dockerfile, docker-compose.yml 초안 생성 |
| Django 로직 | 등수 판정 알고리즘, 뷰 구조 제안 |
| 디버깅 | 오류 원인 분석 및 해결 방법 제시 |
| 문서 작성 | README 및 보고서 작성 지원 |