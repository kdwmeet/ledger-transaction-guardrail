from langgraph.graph import StateGraph, END
from src.agents.state import LedgerState
from src.agents.nodes import ledger_dispatcher_node, ledger_parser_node

def create_ledger_graph():
    workflow = StateGraph(LedgerState)

    workflow.add_node("parser", ledger_parser_node)
    workflow.add_node("dispatcher", ledger_dispatcher_node)

    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "dispatcher")
    workflow.add_edge("dispatcher", END)

    return workflow.compile()

compiled_ledger_graph = create_ledger_graph()