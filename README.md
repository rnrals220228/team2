# 보행자 맞춤형 AI 길찾기 시스템 프로토타입

혼잡도, 사용자 특성, 장애물 회피를 반영해 A* 알고리즘으로 개인화 경로를 찾는 Python 프로토타입입니다. 실제 지도/API 대신 6x6 mock 보행자 그래프를 사용합니다.

## 파일 구조

```text
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── graph.py
│   ├── routing.py
│   ├── congestion.py
│   ├── user_profile.py
│   ├── visualization.py
│   └── models.py
├── data/
├── requirements.txt
└── README.md
```

## 설치

```bash
cd project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 샘플 실행

처음 실행하면 mock 데이터로 샘플 경로를 바로 계산하고 `data/route.html`을 생성합니다.

```bash
python -m app.main
```

## API 서버 실행

```bash
uvicorn app.main:app --reload
```

브라우저에서 문서를 확인합니다.

```text
http://127.0.0.1:8000/docs
```

## 테스트 방법

### PowerShell 요청 예시

```powershell
$body = @{
  start = @(0, 0)
  end = @(5, 5)
  current_time = "2026-05-30T14:00:00"
  user = @{
    visual_impairment = $false
    panic_disorder = $true
    stairs_preference = -0.8
    slope_preference = -0.5
  }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/route" -Method Post -ContentType "application/json" -Body $body
```

### 서버 없이 API 함수 테스트

```bash
python -c "from fastapi.testclient import TestClient; from app.main import app; c=TestClient(app); r=c.post('/route', json={'start':[0,0],'end':[5,5],'current_time':'2026-05-30T14:00:00','user':{'visual_impairment':False,'panic_disorder':True,'stairs_preference':-0.8,'slope_preference':-0.5}}); print(r.status_code); print(r.json())"
```

### curl 요청 예시

```bash
curl -X POST "http://127.0.0.1:8000/route" \
  -H "Content-Type: application/json" \
  -d '{
    "start": [0, 0],
    "end": [5, 5],
    "current_time": "2026-05-30T14:00:00",
    "user": {
      "visual_impairment": false,
      "panic_disorder": true,
      "stairs_preference": -0.8,
      "slope_preference": -0.5
    }
  }'
```

## 구현 요약

- `graph.py`: 좌표를 가진 grid graph와 edge 속성 생성
- `congestion.py`: school, market, tourist zone의 시간대별 혼잡도 mock 갱신
- `user_profile.py`: 시각장애, 공황장애, 계단/경사 기피 비용 반영
- `routing.py`: NetworkX A* 기반 개인화 경로 탐색
- `visualization.py`: 전체 경로는 회색, 선택 경로는 빨간색 PNG로 저장
- `main.py`: FastAPI `/route` 엔드포인트와 샘플 실행

## 사용자 규칙

- 시각장애 사용자는 점자블록이 없는 edge를 사용할 수 없습니다.
- 공황장애 사용자는 혼잡도가 높은 edge 비용이 증가합니다.
- 계단 기피도가 음수이면 계단 edge 비용이 증가합니다.
- 경사 기피도가 음수이면 slope 값이 높은 edge 비용이 증가합니다.
