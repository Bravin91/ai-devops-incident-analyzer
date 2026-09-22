def build_incident_prompt(incident):
    """
    Build a structured prompt from the incident detected
    by the deterministic analyzer.
    """

    return f"""
You are a senior DevOps incident response engineer.

Analyze the following incident:

Severity: {incident["severity"]}
Category: {incident["category"]}
Issue: {incident["issue"]}

Evidence:
{chr(10).join("- " + item for item in incident["evidence"])}

Existing recommended actions:
{chr(10).join("- " + item for item in incident["recommendations"])}

Provide:

1. Likely root cause
2. Investigation steps
3. Recommended remediation
4. Additional evidence needed
""".strip()


def analyze_with_ai(incident):
    """
    Temporary AI layer.

    This mock implementation allows us to test the architecture
    before connecting a real LLM API.
    """

    prompt = build_incident_prompt(incident)

    return {
        "root_cause": "The application cannot establish a connection to the database.",
        "investigation": [
            "Verify that the database service is running",
            "Verify database connectivity from the application host",
            "Check port 5432 connectivity",
            "Check firewall and security-group rules"
        ],
        "remediation": [
            "Restore database availability if the service is down",
            "Correct database connectivity configuration if required",
            "Verify network access between the application and database"
        ],
        "additional_evidence": [
            "Database service status",
            "Application database configuration",
            "Network connectivity test results"
        ],
        "prompt": prompt
    }
