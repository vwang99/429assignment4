from dataclasses import dataclass
from typing import List, Set, Dict, Any

@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""

class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        """Store initial facts into the working memory."""
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        """ Return True if all antecedents are true and consequent not yet known."""
        return all(a in self.facts for a in rule.antecedents) and rule.consequent not in self.facts

    def run(self) -> None:
        """Implement the forward chaining loop."""
        fired = True
        while fired:
            fired = False
            for rule in sorted(self.rules, key=lambda r: (-r.priority, r.name)):
                if self.can_fire(rule):
                    self.facts.add(rule.consequent)
                    self.trace.append({
                        "rule": rule.name,
                        "added": rule.consequent,
                        "antecedents": rule.antecedents
                    })
                    fired = True
        pass

    def conclusions(self) -> Dict[str, List[str]]:
        """Return separated results (recommendations, specs, other facts)."""
        recs = [f for f in self.facts if f.startswith("recommend:")]
        specs = [f for f in self.facts if f.startswith("spec:")]
        others = [f for f in self.facts if not (f.startswith("recommend:") or f.startswith("spec:"))]
        return {"recommendations": recs, "specs": specs, "others": others}

