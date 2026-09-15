def analyze_log(log_text):
    """
    Analyze application logs and identify potential incidents.
    """

    log_text = log_text.lower()

    result = {
        "severity": "LOW",
        "issue": "No significant issue detected",
        "recommendations": []
    }

    # Database connectivity
    if "connection refused" in log_text:
        result["severity"] = "HIGH"
        result["issue"] = "Database connectivity failure"

        result["recommendations"] = [
            "Check whether the database service is running",
            "Verify database port 5432",
            "Check firewall or security-group rules",
            "Verify the database hostname and endpoint"
        ]

    # Out of memory
    elif "out of memory" in log_text or "oom" in log_text:
        result["severity"] = "CRITICAL"
        result["issue"] = "Memory exhaustion"

        result["recommendations"] = [
            "Check current memory utilization",
            "Identify processes consuming excessive memory",
            "Check Kubernetes pod memory limits if applicable",
            "Review recent application changes for memory leaks"
        ]

    # Disk space
    elif "no space left on device" in log_text or "disk full" in log_text:
        result["severity"] = "HIGH"
        result["issue"] = "Disk space exhaustion"

        result["recommendations"] = [
            "Check filesystem usage with df -h",
            "Identify large directories and files",
            "Review application and system logs",
            "Clean up unnecessary files or expand disk capacity"
        ]

    # HTTP 5xx
    elif "500 internal server error" in log_text or "http 500" in log_text:
        result["severity"] = "HIGH"
        result["issue"] = "Application server error"

        result["recommendations"] = [
            "Check application logs",
            "Check recent deployments",
            "Verify backend dependencies",
            "Check application health and resource utilization"
        ]

    # Timeout
    elif "timeout" in log_text or "timed out" in log_text:
        result["severity"] = "HIGH"
        result["issue"] = "Request or service timeout"

        result["recommendations"] = [
            "Check network connectivity",
            "Check target service availability",
            "Review application timeout configuration",
            "Check CPU and memory utilization"
        ]

    return result
