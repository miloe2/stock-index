## 프로젝트 방향/확장
### MVP
- VIX, FGI 를 토대로 계산식 생성
- api 호출 시, 오늘 날짜 기준 매수/매도 지표 조합 스코어링

### 확장한다면, 
- FRED api로 vix, sp500 이격도 1년치 날짜&값 DB에 insert
- 계산식(새로운 지수)로 1년치 계산해서 db insert
- 1년치 스코어링 지수 api 추가 (FE 차트 추가용)
- fear and greed 지수 csv or 크롤링으로 1년치 db 넣기 (선택사항)
- spy, qqq 백테스트

### 프로젝트 인프라
- DB 연결
- 10분마다 핑 날려서 안꺼지게 하기
- 하루에 한번 씩 FGI, VIX 호출 * insert 자동화




✅ 정리된 프로젝트 구조 (with 제안 포함)
📌 1. 최소 기능 (MVP)
현재 기능으로 "오늘 기준 매수/매도 판단" API

✅ 현재 포함 내용:
VIX + FGI → MSS 계산

오늘 기준 스코어 제공 API

 스코어 해석 기준 리턴

{
  "score": 78,
  "signal": "BUY",
  "message": "공포 극단 수준 - 분할 매수 고려"
}
📌 2. 1단계 확장 (데이터 저장 및 자동 계산)
1년치 데이터 기반으로 MSS 저장 및 API 제공

✅ 현재 포함 내용:
VIX + SP500 이격도 → FRED API → DB Insert

FGI → 수동 CSV 또는 크롤링 → DB Insert

1년치 MSS 계산 후 DB Insert

💡 제안 추가:
 MSS 계산 로그를 기록 (값 변경 여부, 기준 지표 값 포함)

 MSS 저장용 별도 테이블 구조 (id, date, vix, fgi, deviation, score, signal)

📌 3. 2단계 확장 (API 및 프론트 제공)
MSS 지표 시계열 API + 프론트 차트 시각화

✅ 현재 포함 내용:
/score/history API → 1년치 MSS 리턴

💡 제안 추가:
 MSS 지표에 색상/상태 구간 포함 (030: 탐욕, 70100: 공포)

 매매 트리거 지점도 API 리턴


{
  "date": "2025-04-01",
  "score": 85,
  "signal": "BUY"
}
 프론트 차트 개선:

Line Chart + 탐욕/공포 영역 음영

매수/매도 시점 마커

📌 4. 3단계 확장 (전략 백테스트)
SPY, QQQ 등 실제 자산에 전략 적용

✅ 현재 포함 내용:
백테스트 계획 중

💡 제안 추가:
 전략 수익률 vs Buy & Hold 수익률 그래프

 결과 API 예:

{
  "cagr": "7.5%",
  "max_drawdown": "-12.4%",
  "mdd_date": "2022-06-01",
  "strategy_vs_buy_hold": "1.24x"
}
 기본 자산: SPY / QQQ / KOSPI 선택 옵션 추가

 전략 설정값 조정 API (VIX > 30 → 매수 등)

⚙️ 인프라 / 운영 자동화
✅ 현재 포함 내용:
DB 연결

10분 Ping

하루 1회 VIX/FGI Insert 자동화

💡 제안 추가:
 DB 테이블 정의 문서화 (metrics, scores, assets, backtests)

 /health API로 서비스 상태 체크 가능

 cron + 로그 파일 저장 (실패 알림 or retry 시스템)

 FGI 예외 발생 시 fallback 값 사용 (ex: 이전값 재사용)

 FastAPI + Docker + PostgreSQL 배포 구조로 확장 고려

📌 전체 구조 요약

[Data Layer]
 ├── FRED API (VIX, SP500)
 ├── FGI API or 크롤링
 └── DB (metrics, scores)

[Logic Layer]
 ├── MSS 계산 엔진
 ├── 전략 로직
 └── 백테스트 시뮬레이터

[API Layer]
 ├── /score/today
 ├── /score/history
 ├── /backtest?asset=SPY&...
 └── /health

[Automation]
 ├── Daily Job: VIX + FGI Insert
 ├── MSS 자동 계산
 └── Ping or uptime bot
🟢 결론: 다음 추천 우선 작업
 FGI 하루 저장 자동화 구현

 /score/history API + MSS 일별 계산

 백테스트 구조 설계 및 API 기본형





