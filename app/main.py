from analyzer import analyze_log


def main():
    with open("logs/sample.log", "r") as log_file:
        log_text = log_file.read()

    result = analyze_log(log_text)

    print("\n===== INCIDENT ANALYSIS =====")
    print(f"Severity: {result['severity']}")
    print(f"Issue: {result['issue']}")

    print("\nRecommended Actions:")

    for recommendation in result["recommendations"]:
        print(f"- {recommendation}")


if __name__ == "__main__":
    main()
