from src.finance.governance import CostTracker, CostEstimate
from src.autonomy.discovery import CapabilityExplorer
from src.tools.registry import ToolRegistry, ToolMetadata
from src.autonomy.async_intervention import AsyncIntervention
from src.core.state import StateStore
from src.core.agent import AgentState
import time

def main():
    # 1. Setup Environment
    store = StateStore("production_ready.db")
    registry = ToolRegistry()
    registry.register_tool(lambda: "Success", ToolMetadata("db_query", "Query DB", ["database_access"]))
    
    finance = CostTracker(budget_limit=1.0)
    explorer = CapabilityExplorer(registry)
    intervener = AsyncIntervention(store)
    
    # 2. Dynamic Discovery
    credentials = {"DB_CONNECTION_STRING": "postgresql://..."}
    capabilities = explorer.discover_capabilities(credentials)
    allowed_tools = explorer.get_authorized_tools(capabilities)
    
    # 3. Execution with Cost Tracking
    print("\n--- Starting Execution ---")
    estimate = CostEstimate(input_tokens=1500, output_tokens=500, tool_calls=1)
    if finance.is_within_budget(estimate.calculate_total()):
        finance.record_transaction(estimate)
        print("Executing task with authorized tools:", allowed_tools)
    else:
        print("ABORT: Budget exceeded.")
        
    # 4. Async Intervention
    state = AgentState(current_task="Complex Migration")
    request_id = intervener.suspend_for_human(state, "Requires confirmation for non-dry-run")
    
    print(f"\n[Simulator] Intervention requested in background. Request ID: {request_id}")
    time.sleep(1)
    
    print("[Simulator] ... 2 hours later (human approves) ...")
    intervener.resolve_request(request_id, feedback="Approved. Proceed with care.")
    
    final_state = store.load_state(state.agent_id)
    print("\nFinal Resumed State Context:", final_state.context)

if __name__ == "__main__":
    main()
