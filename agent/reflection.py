from tools.llm import call_llm

def reflect(request: str, sections: dict):
    prompt = f"""
You are a senior software architect performing a quality review of a system design report.

USER REQUEST:
{request}

GENERATED REPORT:
{sections}

Evaluate the report based on:

1. Completeness (are all key system design areas covered?)
2. Technical correctness (are concepts accurate?)
3. Missing sections (anything important missing?)
4. Consistency (any contradictions or unclear parts?)

OUTPUT RULES:

If the report is HIGH QUALITY:
Return exactly:
PASS

If the report has issues:
Return ONLY in this format:

MISSING:
- ...
IMPROVEMENTS:
- ...
ISSUES:
- ...
"""

    return call_llm(prompt)