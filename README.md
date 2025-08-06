# ⚾ KBO LIVE RANK

**KBO LIVE RANK**는 KBO 리그 팀들의 실시간 경기 결과를 반영하여 예상 승패를 기반으로 순위를 자동 계산해 보여주는 웹 애플리케이션입니다.  
**Python WebSocket**과 **React + React Bootstrap**을 사용하여 **실시간 순위 변동**을 시각적으로 확인할 수 있습니다.

---

## 🚀 주요 기능

- ⚡ 실시간 경기 스코어를 반영해 현재 이기고 있는 팀은 1승, 지고 있는 팀은 1패로 가정하여 **예상 순위 자동 계산**
- 🔁 이전 순위와 비교한 **순위 변동 (상승/하락) 시각화**
- 🔗 Python WebSocket 서버와 React 클라이언트 간 **실시간 데이터 연동**
- 📱 React Bootstrap 기반 **직관적이고 반응형 UI**

---

## 📁 프로젝트 구조

```bash
kbosunwe/
├── node_modules/             # React 의존성 모듈
├── public/                   # 정적 파일
├── src/                      # 프론트엔드 소스
│   ├── App.js                # 메인 React 컴포넌트
│   ├── App.css               # 스타일
│   ├── index.js              # 앱 진입점
│   ├── index.css             # 기본 CSS
│   ├── logo.svg              # 로고
│   ├── reportWebVitals.js    # 성능 측정
│   ├── App.test.js           # 테스트 코드
│   ├── setupTests.js         # 테스트 환경 설정
├── wsc.py                    # WebSocket 서버 (Python)
├── asdf.html                 # 테스트/임시 HTML 파일
├── package.json              # 프로젝트 정보 및 스크립트
├── package-lock.json         # 의존성 고정
└── README.md                 # 프로젝트 설명 파일
```

---

## 🧰 사용 기술 스택

| 구분        | 기술                         |
|-------------|------------------------------|
| 프론트엔드  | React, React Bootstrap       |
| 백엔드      | Python, WebSocket            |
| 통신 방식   | WebSocket (양방향 통신)      |
| 스타일링    | CSS, Bootstrap               |

---

## 📦 설치 및 실행

### 1. 백엔드 서버 실행 (WebSocket)

```bash
# Python 패키지 설치 (필요 시)
pip install websockets

# WebSocket 서버 실행
python wsc.py
```

### 2. 프론트엔드 실행 (React)

```bash
# 의존성 설치
npm install

# React 개발 서버 실행
npm start
```

---

## 💡 개발 의도

실제 데이터를 바탕으로 **프론트-백 실시간 연동**을 직접 구현하며 학습 및 실습 목적으로 제작되었습니다.  
직접 WebSocket 서버를 구성하고 React와 연결하여, 프론트에서 순위를 계산하고 UI로 보여주는 과정을 체계적으로 경험할 수 있습니다.

---

## 🔧 TODO / 향후 개선 사항

- [ ] 팀별 로고 및 선수 상세 정보 연동
- [ ] 경기 상세 페이지 연결

---

## 📄 라이선스

MIT License  
© 2025 **sungjujjang**

###### README.md 작성자 : CHATGPT