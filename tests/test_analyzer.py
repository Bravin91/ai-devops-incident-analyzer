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


def test_memory_exhaustion():
    log_text = """
    ERROR: Out of memory
    ERROR: Application process killed
    """

    result = analyze_log(log_text)

    assert result["severity"] == "CRITICAL"
    assert result["issue"] == "Memory exhaustion"


def test_disk_space_exhaustion():
    log_text = """
    ERROR: No space left on device
    ERROR: Failed to write log file
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Disk space exhaustion"


def test_http_500_error():
    log_text = """
    ERROR: HTTP 500
    ERROR: Internal server failure
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Application server error"


def test_timeout():
    log_text = """
    ERROR: Request timed out
    ERROR: Backend service timeout
    """

    result = analyze_log(log_text)

    assert result["severity"] == "HIGH"
    assert result["issue"] == "Request or service timeout"


def test_no_incident():
    log_text = """
    INFO: Application started
    INFO: Health check passed
    """

    result = analyze_log(log_text)

    assert result["severity"] == "LOW"
    assert result["issue"] == "No significant issue detected"
