from src.planning.trace import ReasoningTrace
from src.failure.degradation import ReasoningDegradationSimulator
from src.tools.registry import ToolRegistry, ToolMetadata
import json

def mock_deploy_tool(env="staging"):
    return f"Deployed to {env} successfully."

def main():
    # 1. Initialize Trace
    trace = ReasoningTrace()
    
    # 2. Setup Tool Registry
    registry = ToolRegistry()
    registry.register_tool(
        mock_deploy_tool, 
        ToolMetadata(
            name="deploy", 
            description="Deploys code", 
            capability_requirements=["cloud_access"],
            risk_level=8
        )
    )
    
    # 3. Setup Degradation Simulator
    degrader = ReasoningDegradationSimulator("agent-007")
    degrader.increase_entropy(0.6) # High instability
    
    print("\n--- Starting Advanced Chain ---")
    
    # Step 1: Planning
    thought = degrader.inject_hallucination("I need to deploy the application to production.")
    trace.add_step(
        thought=thought,
        action="call_tool:deploy",
        observation="Pending",
        confidence=degrader.corrupt_confidence(0.9)
    )
    
    # Step 2: Execution with capability check
    agent_capabilities = ["cloud_access"]
    try:
        print(f"Agent attempting tool call with capabilities: {agent_capabilities}")
        result = registry.call_tool("deploy", agent_capabilities, env="production")
        trace.steps[-1].observation = result
    except Exception as e:
        trace.steps[-1].observation = str(e)
        print(f"Error: {e}")

    # 4. Final Analysis
    print("\n--- Final Stability Analysis ---")
    analysis = trace.analyze_stability()
    print(json.dumps(analysis, indent=2))
    
    trace.export_json("advanced_trace.json")

if __name__ == "__main__":
    main()
