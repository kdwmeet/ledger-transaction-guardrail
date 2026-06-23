from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class LedgerState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    order_id: str
    account_id: str
    raw_transaction_log: str
    parsed_metrics: dict
    hazard_score: int
    safety_level: str
    action_status: str