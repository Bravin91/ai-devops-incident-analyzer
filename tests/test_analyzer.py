from app.analyzer import analyze_log


def test_database_connection_failure():
    log_text = """
    ERROR: Connection refused
    ERROR: Database connection failed
    ERROR: Retry limit exceeded
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Database connectivity failure"


def test_no_incident():
    log_text = """
    INFO: Application started
    INFO: Health check passed
    """

    result = analyze_log(log_text)

    assert result["severity"] == "LOW"
    assert result["issue"] == "No significant issue detected"
