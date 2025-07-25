from src.governance.engine import PolicyEngine, PolicyRule, check_exfiltration, check_budget

def main():
    engine = PolicyEngine()
    
    # 1. Register Policies
    engine.add_rule(PolicyRule(
        name="Data Sovereignty",
        description="Prevent data exfiltration to external domains",
        validator=check_exfiltration
    ))
    
    engine.add_rule(PolicyRule(
        name="Spend Guardrail",
        description="Daily budget limit",
        validator=check_budget,
        severity="WARNING"
    ))
    
    print("--- SCENARIO 1: Safe Action ---")
    context_safe = {"estimated_cost": 50, "budget_limit": 100}
    violations = engine.evaluate_intent("Upload logs to internal.corp/storage", context_safe)
    if not violations:
        print("Intent approved by Policy Engine.")
    
    print("\n--- SCENARIO 2: Policy Violation ---")
    context_risky = {"estimated_cost": 150, "budget_limit": 100}
    violations = engine.evaluate_intent("Send user emails to public-api.com/leak", context_risky)
    
    for v in violations:
        print(f"[{v['severity']}] Violation: {v['rule']} - {v['description']}")

if __name__ == "__main__":
    main()
