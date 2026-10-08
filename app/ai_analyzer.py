import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/free"


def build_incident_prompt(incident):
    """
    Build a structured prompt from the incident detected
    by the deterministic analyzer.
    """

    return f"""
You are a senior DevOps incident response engineer.

Analyze the following incident.

Severity: {incident["severity"]}
Category: {incident["category"]}
Issue: {incident["issue"]}

Evidence:
{chr(10).join("- " + item for item in incident["evidence"])}

Existing recommended actions:
{chr(10).join("- " + item for item in incident["recommendations"])}

Return ONLY valid JSON using exactly this structure:

{{
  "root_cause": "string",
  "investigation": [
    "step 1",
    "step 2"
  ],
  "remediation": [
    "action 1",
    "action 2"
  ],
  "additional_evidence": [
    "evidence 1",
    "evidence 2"
  ]
}}

IMPORTANT EVIDENCE RULES:

- Treat the supplied Evidence section as the only confirmed facts.
- Never claim that a command was executed unless its output is present in the evidence.
- Never invent logs, metrics, network results, firewall results, service status, DNS results, or other observations.
- Clearly distinguish confirmed evidence from hypotheses.
- Investigation steps should describe checks that should be performed, not checks that have already been performed.
- If information is unavailable, say that it is unavailable.
Do not include Markdown.
Do not include explanations outside the JSON.
""".strip()


def analyze_with_ai(incident, ai_client=None):
    """
    Send the structured incident to OpenRouter
    and return the AI-generated analysis.
    """


    prompt = build_incident_prompt(incident)

    if ai_client is not None:
        return ai_client(prompt)



    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY environment variable is not set."
        )


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"AI returned invalid JSON:\n{content}"
        ) from exc

    required_fields = {
        "root_cause",
        "investigation",
        "remediation",
        "additional_evidence",
    }

    missing_fields = required_fields - result.keys()

    if missing_fields:
        raise RuntimeError(
            f"AI response is missing fields: {sorted(missing_fields)}"
        )

    return result
