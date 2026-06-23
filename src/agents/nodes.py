import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from src.config import Config
from src.agents.state import LedgerState
from src.services.ledger_gate import update_secure_ledger, execute_ledger_rollback

llm = ChatOpenAI(
    model=Config.MODEL_NAME,
    api_key=Config.OPENAI_API_KEY
)

def ledger_parser_node(state: LedgerState) -> dict:
    """비정형 트랜잭션 로그 텍스트를 실시간 분석하여 물리 메트릭과 위해도를 파싱하는 노드"""
    log_text = state.get("raw_transaction_log", "")

    system_prompt = (
        "You are an automated real-time e-commerce financial ledger and double-spending compliance orchestrator.\n"
        "Analyze the incoming transaction log and calculate a transaction hazard score based on race conditions, duplicate idempotency keys, or distributed lock timeouts.\n"
        "Return ONLY a strict JSON format with keys:\n"
        "'metrics' (dict with request_gap_ms, retry_count, idempotency_status, total_amount), 'hazard_score' (integer 0 to 100 based on hazard urgency), and 'safety_level' (allowed: SECURE, SUSPICIOUS, DOUBLE_SPENDING)."
    )

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": log_text}
    ])

    try:
        data = json.loads(response.content)
        score = int(data.get("hazard_score", 0))
        safety_label = data.get("safety_level", "SECURE")

        action = "ROLLBACK_LEDGER" if score >= 70 or safety_label == "DOUBLE_SPENDING" else "COMMIT_LEDGER"
        return {
            "parsed_metrics": data.get("metrics", {}),
            "hazard_score": score,
            "safety_level": safety_label,
            "action_status": action
        }
    except Exception:
        return {"parsed_metrics": {}, "hazard_score": 0, "safety_level": "SECURE", "action_status": "COMMIT_LEDGER"}

def ledger_dispatcher_node(state: LedgerState) -> dict:
    """가드레일 상태(action_status) 판별 결과에 의거해 일반 원장 커밋과 긴급 롤백 제어로 분기하는 실행 노드"""
    action = state.get("action_status")
    order= state.get("order_id", "ORD-0000")
    account = state.get("account_id", "UNKNOWN")
    score = state.get("hazard_score", 0)
    safety_label = state.get("safety_level", "SECURE")
    metrics = state.get("parsed_metrics", {})

    if action == "COMMIT_LEDGER":
        execution_log = update_secure_ledger(order, safety_label)
        return {"messages": [AIMessage(content=execution_log)]}
    else:
        reason = f"동시성 레이스 컨디션 및 이중 정산 부적격 단계 [{safety_label}] 위협 지수 [{score}점] 감지 (요청 시차: {metrics.get('request_gap_ms', '0')}ms)"
        execution_log = execute_ledger_rollback(order, account, reason)
        return {"messages": [AIMessage(content=execution_log)]}