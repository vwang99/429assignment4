from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"


def collect_initial_facts():
    facts = []
    if input("Is portability important? (y/n): ").lower().startswith("y"):
        facts.append("portable")
    if input("Do you need long battery life? (y/n): ").lower().startswith("y"):
        facts.append("long_battery")
    
    budget_set = False
    if input("Is your budget high? (y/n): ").lower().startswith("y"):
        facts.append("budget_high")
        budget_set = True
    if not budget_set and input("Is your budget medium? (y/n): ").lower().startswith("y"):
        facts.append("budget_medium")
        budget_set = True
    if not budget_set and input("Is your budget low? (y/n): ").lower().startswith("y"):
        facts.append("budget_low")
        
    os_set = False
    if input("Do you prefer Windows? (y/n): ").lower().startswith("y"):
        facts.append("pref_os_windows")
        os_set = True
    if not os_set and input("Do you prefer macOS? (y/n): ").lower().startswith("y"):
        facts.append("pref_os_macos")
        os_set = True
    if not os_set and input("Do you prefer Linux? (y/n): ").lower().startswith("y"):
        facts.append("pref_os_linux")
    
    if input("Do you play games? (y/n): ").lower().startswith("y"):
        facts.append("gaming")
    if input("Do you do creative work? (y/n): ").lower().startswith("y"):
        facts.append("creative_work")
    if input("Is this for office-only tasks? (y/n): ").lower().startswith("y"):
        facts.append("office_only")
    if input("Do you need AI acceleration? (y/n): ").lower().startswith("y"):
        facts.append("needs_ai_accel")
    if input("Do you want a large screen? (y/n): ").lower().startswith("y"):
        facts.append("large_screen")
    if input("Do you travel often? (y/n): ").lower().startswith("y"):
        facts.append("travel_often")
    return facts


def print_results(engine: ForwardChainingEngine):
    results = engine.conclusions()

    for r in results["recommendations"]:
        fact_name = r.replace("recommend:", "")
        rule_name = next((t["rule"] for t in engine.trace if t["added"] == r), "")
        print(f"> Recommendation: {fact_name}")
        print(f"> Explanation: derived from rule '{rule_name}'")

    for s in results.get("specs", []):
        spec_name = s.replace("spec:", "")
        rule_name = next((t["rule"] for t in engine.trace if t["added"] == s), "")
        print(f"> Spec: {spec_name}")
        print(f"> Explanation: derived from rule '{rule_name}'")


def main():
    rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)

    initial_facts = collect_initial_facts()

    engine.assert_facts(initial_facts)
    engine.run()

    print_results(engine)


if __name__ == "__main__":
    main()
