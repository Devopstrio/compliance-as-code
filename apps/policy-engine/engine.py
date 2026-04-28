import yaml
import logging

class PolicyEngine:
    def __init__(self):
        self.logger = logging.getLogger("policy-engine")

    def evaluate_rule(self, resource_config: dict, policy: dict):
        """
        Evaluates a single resource against a declarative policy.
        """
        rule_type = policy.get("type")
        target_field = policy.get("field")
        expected_value = policy.get("expected")

        actual_value = resource_config.get(target_field)

        if rule_type == "equals":
            is_compliant = (actual_value == expected_value)
        elif rule_type == "contains":
            is_compliant = (expected_value in actual_value)
        else:
            is_compliant = False

        return {
            "compliant": is_compliant,
            "actual": actual_value,
            "expected": expected_value,
            "message": "Validation Successful" if is_compliant else f"Mismatch: expected {expected_value}, got {actual_value}"
        }

    def calculate_framework_score(self, results: list):
        """
        Calculates a weighted score for a set of results.
        """
        if not results: return 0
        passed = sum(1 for r in results if r['compliant'])
        return round((passed / len(results)) * 100, 2)

if __name__ == "__main__":
    engine = PolicyEngine()
    
    # Test Evaluation
    config = {"encryption": "enabled", "mfa": "disabled"}
    policy = {"type": "equals", "field": "mfa", "expected": "enabled"}
    
    result = engine.evaluate_rule(config, policy)
    print(f"Compliance Result: {result['compliant']} - {result['message']}")
