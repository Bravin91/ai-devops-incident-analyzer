from app.analyzer import analyze_log
from app.ai_analyzer import build_incident_prompt, analyze_with_ai


def test_database_connection_failure():
    log_text = """
    ERROR: Connection refused
    ERROR: Database connection failed
    ERROR: Retry limit exceeded
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Database connectivity failure"
    assert result["category"] == "DATABASE"
    assert "ERROR: Connection refused" in result["evidence"]
    assert "ERROR: Database connection failed" in result["evidence"]
    assert "ERROR: Retry limit exceeded" in result["evidence"]


def test_memory_exhaustion():
    log_text = """
    ERROR: Out of memory
    ERROR: Application process killed
    """

    result = analyze_log(log_text)

    assert result["severity"] == "CRITICAL"
    assert result["issue"] == "Memory exhaustion"
    assert result["category"] == "MEMORY"


def test_disk_space_exhaustion():
    log_text = """
    ERROR: No space left on device
    ERROR: Failed to write log file
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Disk space exhaustion"
    assert result["category"] == "DISK"


def test_http_500_error():
    log_text = """
    ERROR: HTTP 500
    ERROR: Internal server failure
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Application server error"
    assert result["category"] == "APPLICATION"


def test_timeout():
    log_text = """
    ERROR: Request timed out
    ERROR: Backend service timeout
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Request or service timeout"
    assert result["category"] == "NETWORK"


def test_no_incident():
    log_text = """
    INFO: Application started
    INFO: Health check passed
    """

    result = analyze_log(log_text)

    assert result["severity"] == "LOW"
    assert result["issue"] == "No significant issue detected"
    assert result["category"] == "NONE"
    assert result["evidence"] == []


def test_ai_prompt_contains_incident_information():
    incident = {
        "severity": "HIGH",
        "category": "DATABASE",
        "issue": "Database connectivity failure",
        "evidence": [
            "ERROR: Connection refused",
            "ERROR: Database connection failed"
        ],
        "recommendations": [
            "Check whether the database service is running"
        ]
    }

    prompt = build_incident_prompt(incident)

    assert "DATABASE" in prompt
    assert "Database connectivity failure" in prompt
    assert "ERROR: Connection refused" in prompt


def test_ai_analysis_returns_expected_structure():
    incident = {
        "severity": "HIGH",
        "category": "DATABASE",
        "issue": "Database connectivity failure",
        "evidence": [
            "ERROR: Connection refused"
        ],
        "recommendations": [
            "Check whether the database service is running"
        ]
    }

    def fake_ai_client(prompt):
        return {
            "root_cause": "Database service is unavailable",
            "investigation": [
                "Check database service status"
            ],
            "remediation": [
                "Restore database service"
            ],
            "additional_evidence": [
                "Database service status"
            ]
        }

    result = analyze_with_ai(incident, ai_client=fake_ai_client)

    assert "root_cause" in result
    assert "investigation" in result
    assert "remediation" in result
    assert "additional_evidence" in result

    assert len(result["investigation"]) > 0
    assert len(result["remediation"]) > 0
