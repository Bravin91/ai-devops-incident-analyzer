from analyzer import analyze_log
from ai_analyzer import analyze_with_ai


def main():
    with open("logs/sample.log", "r") as log_file:
        log_text = log_file.read()

    incident = analyze_log(log_text)
    ai_result = analyze_with_ai(incident)

    print("\n===== INCIDENT ANALYSIS =====")
    print(f"Severity: {incident['severity']}")
    print(f"Category: {incident['category']}")
    print(f"Issue: {incident['issue']}")

    print("\nEvidence:")

    for evidence in incident["evidence"]:
        print(f"- {evidence}")

    print("\nRecommended Actions:")

    for recommendation in incident["recommendations"]:
        print(f"- {recommendation}")

    print("\n===== AI ANALYSIS =====")

    print("\nLikely Root Cause:")
    print(ai_result["root_cause"])

    print("\nInvestigation Steps:")

    for step in ai_result["investigation"]:
        print(f"- {step}")

    print("\nRemediation:")

    for action in ai_result["remediation"]:
        print(f"- {action}")

    print("\nAdditional Evidence Needed:")

    for evidence in ai_result["additional_evidence"]:
        print(f"- {evidence}")


if __name__ == "__main__":
    main()
