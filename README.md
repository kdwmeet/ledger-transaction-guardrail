# Real-Time Transaction Telemetry Analytics & Double-Spending Hold Guardrail Orchestrator

LangGraph와 최신 초고속/비용 효율화 모델인 gpt-5.4-nano를 기반으로 구축된 실시간 자율 멀티 소스 트랜잭션 데이터 분석 및 가동 부하 위험도(Blackout) 진단 기반 부하 분산(Load-Shedding) 가드레일 가이드 시스템입니다. 글로벌 이커머스 정산 플랫폼 및 분산 코어 뱅킹 인터페이스에서 실시간으로 유입되는 비정형 멱등성 토큰 메타데이터, 분산 락 해제 지연, 리트라이 횟수 텔레메트리 스트림을 상시 감시하여 가동 품질 레이블을 초고속 구조화하고, 레이스 컨디션 및 이중 정산 한계선 파괴 징후 탐지 시 코어 관제망 연동을 통해 중앙 전산 적재 전 하드웨어 트랜잭션을 즉시 자율 물리 롤백(Fail-Safe Rollback) 조치하는 지능형 에너지 관리 거버넌스 인프라를 구현했습니다.

---

## Key Features & Architecture

- **실시간 계통 센서 스크리닝:** 인바운드 설비 텔레메트리 로그의 비정형 맥락(동일 멱등 키 다중 인입, 분산 락 타임아웃, 비대칭 정산 이탈 위험)을 분석하여 하드웨어의 트랜잭션 위험 인텐트를 gpt-5.4-nano를 통해 초고속으로 판별합니다.
- **문맥 기반 계통 붕괴 위험 스코어링:** 사전에 하드코딩된 단편적 임계치 비교 정책의 취약성을 보완하기 위해, 복합 센서 메트릭 결합 성향과 전력망 붕괴 위험도를 종합 평가하여 0~100점 척도의 위험 지수(Transaction Hazard Index)를 실시간 연산해 가드레일에 동기화합니다.
- **자율 하드웨어 원장 제어 및 동적 격리:** 가드레일 레이어의 action_status 분석 결과에 따라 안전 계통 장비의 관제 원장 정상 동기화(COMMIT_LEDGER)와 전력망 위험 설비의 실시간 비핵심 부하 제어 및 ESS 방전(ROLLBACK_LEDGER) 조치를 분리 실행합니다.
- **State-Driven EMS Control Engine:** 센서 로그 수집부터 위해성 스코어링, 가드레일 판별, 코어 전력 전산망 API 자율 제어 명령 하사에 이르는 전 과정이 LangGraph의 확정적 상태 기계 구조 위에서 오차 없이 동기 운용됩니다.

---

## Tech Stack

- Framework: LangGraph (v0.2+), LangChain (v0.3+)
- LLM Core: OpenAI gpt-5.4-nano (초저지연, 고효율 추론 모델)
- Environment & Dependency Manager: uv (Fast Python package installer)
- Frontend Dashboard: Streamlit (v1.35+)

---

## Project Directory Structure

상용 분산 원장 및 차세대 결제 게이트웨이 표준 아키텍처 규격을 준수하여 인바운드 트래픽 수집 레이어, 텔레메트리 스코어링 가드레일 노드, 가상 코어 뱅킹 원장 제어 모듈을 독립 분리했습니다.
```
ledger-transaction-guardrail/
├── src/
│   ├── main.py                 # Streamlit 실시간 결제 관제 및 정산 상태 모니터 대시보드
│   ├── config.py               # API 키 및 위협 스코어 임계치 설정 관리
│   ├── agents/                 # LangGraph 기반 지능형 트랜잭션 통제 센터
│   │   ├── state.py            # 주문 ID, 계정 정보, 트랜잭션 평판 상태 정의
│   │   ├── graph.py            # 위험 점수에 따른 조건부 제어 분기 그래프 빌드
│   │   └── nodes.py            # 로그 구조화, 금융 가드레일 채점, 제어 명령 생성 노드
│   └── services/               # 코어 원장 및 분산 코어 뱅킹 레이어
│       └── ledger_gate.py      # 가상 원장 롤백 및 트랜잭션 강제 격리 툴
├── requirements.txt            # 명시적 패키지 의존성 목록
└── .env                        # 환경 변수 보안 설정 파일
```
---

## Quick Start

### 1. Prerequisites & Installation

본 프로젝트는 초고속 파이썬 패키지 매니저인 uv를 사용해 가상환경을 구축합니다.

# 저장소 클론 및 이동
```
git clone https://github.com/your-username/ledger-transaction-guardrail.git
cd ledger-transaction-guardrail
```
# uv를 이용한 가상환경 생성 및 활성화
```
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
# 의존성 패키지 일괄 설치
```
uv pip install -r requirements.txt
```
### 2. Environment Variables Setup

PROJ_ROOT 디렉토리에 .env 파일을 생성하고 발급받은 OpenAI API 키를 입력합니다.
```
OPENAI_API_KEY=your_openai_api_key_here
```
### 3. Running the Application

파이썬의 모듈 탐색 경로(sys.path) 충돌을 방지하기 위해 PYTHONPATH 환경변수를 주입하여 모듈 모드로 실행합니다.
```
**Windows (PowerShell):**
$env:PYTHONPATH="."
streamlit run src/main.py
```
```
**Windows (CMD):**
set PYTHONPATH=.
streamlit run src/main.py
```
```
**Mac / Linux:**
PYTHONPATH=. streamlit run src/main.py
```
---

## Production-Ready Architecture Point (포트폴리오 핵심 어필 포인트)

1. **미션 크리티컬 분산 정산 인프라 및 트랜잭션 컴플라이언스 설계 입증**
   - 웹 소프트웨어 프레임워크 바운더리를 넘어 실제 백엔드 분산 자산망의 정합성을 보존하고 자율 롤백하는 '금융 가드레일 오케스트레이션'을 구현함으로써 계통 제어 및 플랫폼 엔지니어링 직무에서 매우 높은 신뢰도 평가를 받습니다.
2. **초저지연 관제 레이턴시 및 상시 운용 비용 최적화**
   - 대규모 이커머스 및 백본 결제망에서 실시간으로 인입되는 시계열 트랜잭션 로그를 대형 모델로 전수 처리하는 것은 구조적 예산 파산을 초래합니다. 본 시스템은 속도가 민칩하고 단가가 극도로 저렴한 경량 모델 gpt-5.4-nano를 전면 가드레일에 배치하여 실시간성을 보존하고 상시 스크리닝 운영 마진을 획기적으로 확보했습니다.

## 실행 화면