import streamlit as st
import random
from langchain_core.messages import AIMessage
from src.agents.graph import compiled_ledger_graph

st.set_page_config(page_title="Ledger Integrity Guardrail Panel", layout="wide")
st.title("실시간 자율 트랜잭션 텔레메트리 분석 및 결제 이상 징후 차단 가드레일")

col1, col2 = st.columns(2)

with col1:
    st.subheader("금융 분산 백본망 및 이커머스 결제 게이트웨이 실시간 로그 스트림")
    
    log_scenario = st.radio(
        "시뮬레이션할 실시간 트랜잭션 패턴 선택",
        ["분산 락(Lock) 타임아웃 붕괴로 인한 동일 멱등성 토큰 이중 정산 시도 (긴급 롤백 차단)", "통상적인 적격 구매 사용자의 단일 결제 승인 요청 (원장 반영 허용)"]
    )
    
    if log_scenario == "분산 락(Lock) 타임아웃 붕괴로 인한 동일 멱등성 토큰 이중 정산 시도 (긴급 롤백 차단)":
        account_id = "user_pay_7721"
        default_log = "[2026-06-22 17:15] CRITICAL - 계정: user_pay_7721, 네트워크 타임아웃 리트라이가 맞물리며 12ms 시차로 동일 주문 번호(ORD-99824)에 대한 이중 승인 API 패킷 인입됨. 분산 데이터베이스 레디스 분산 락 해제 지연 징후 탐지 및 동일한 멱등성 키(Idempotency Key)의 다중 커밋 시도로 원장 파괴 리스크 발생."
    else:
        account_id = "user_pay_1022"
        default_log = "[2026-06-22 17:16] INFO - 계정: user_pay_1022, 단일 상품 구매 라우트(/api/v1/checkout)를 통해 승인 요청 정상 진입됨. 이전 멱등 키 이력 조회가 전무하며 트랜잭션 순차 격리성 정상 유지 확인."
        
    acc_input = st.text_input("결제 요청 계정 식별자", value=account_id)
    raw_log_input = st.text_area("인바운드 비정형 트랜잭션 로그", value=default_log, height=140)
    
    if st.button("금융 거버넌스 가드레일 가동"):
        initial_state = {
            "messages": [],
            "order_id": f"ORD-{random.randint(100000, 999999)}",
            "account_id": acc_input,
            "raw_transaction_log": raw_log_input,
            "parsed_metrics": {},
            "hazard_score": 0,
            "safety_level": "SECURE",
            "action_status": "INIT"
        }
        
        output_state = compiled_ledger_graph.invoke(initial_state)
        st.session_state.ledger_result = output_state
        st.success("실시간 트랜잭션 무결성 검증 및 자율 롤백 통제가 완료되었습니다.")

with col2:
    st.subheader("통합 금융 원장 관제 및 코어 뱅킹 인프라 모니터")
    
    if "ledger_result" in st.session_state:
        res = st.session_state.ledger_result
        status = res.get("action_status")
        score = res.get("hazard_score", 0)
        
        st.markdown(f"**할당 주문 일련번호:** `{res.get('order_id')}`")
        st.markdown(f"**추적 감시 대상 계정:** `{res.get('account_id')}`")
        st.markdown(f"**실시간 원장 무결성 등급:** `{res.get('safety_level')}`")
        
        st.markdown("---")
        st.markdown("**구조화된 트랜잭션 메트릭 JSON 스키마:**")
        st.json(res.get("parsed_metrics", {}))
        
        st.markdown("---")
        st.markdown("**원장 오염 및 레이스 컨디션 위해성 스크리닝:**")
        
        if status == "ROLLBACK_LEDGER":
            st.error(f"종합 원장 위해 지수: {score}점 / 100점 (이중 정산 및 동시성 충돌 위협)")
            st.markdown(f"**종합 오케스트레이터 조치:** `원장 데이터베이스 즉시 롤백 및 트랜잭션 강제 무효화(Rollback Ledger)`")
        else:
            st.success(f"종합 원장 위해 지수: {score}점 / 100점 (정상 적격 트래픽 통과)")
            st.markdown(f"**종합 오케스트레이터 조치:** `메인 정산 원장 최종 커밋 및 데이터 동기화(Commit Ledger)`")
            
        if res.get("messages"):
            st.markdown("---")
            st.warning(f"분산 코어 뱅킹 전산 인프라 최종 원장 제어 로그:\n{res['messages'][-1].content}")
    else:
        st.info("좌측 트래픽 영역에서 게이트웨이 트랜잭션 로그를 발생시키면 자율 가드레일 분석 메트릭이 이곳에 실시간 업데이트됩니다.")