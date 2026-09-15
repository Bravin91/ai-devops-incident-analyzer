def analyze_log(log_text):
    """
    Analyze application logs and identify potential incidents.
    """

    result = {
        "severity": "LOW",
        "issue": "No significant issue detected",
        "recommendations": []
    }

    if "Connection refused" in log_text:
        result["severity"] = "HIGH"
        result["issue"] = "Database connectivity failure"

        result["recommendations"] = [
            "Check whether the database service is running",
            "Verify database port 5432",
            "Check firewall or security-group rules",
            "Verify the database hostname and endpoint"
        ]

    return result
