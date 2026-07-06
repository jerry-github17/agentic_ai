from tools.llm import call_llm
import json
def create_plan(request: str):
    prompt = f"""
You are an autonomous System Design Planner.

Break the request into 5–6 high-level phases for writing a system design report.

Rules:
- Do NOT include low-level sections like APIs, DB, Security
- Only high-level reasoning phases
- Keep it concise and logical

Return ONLY JSON list of steps.
"""
    response = call_llm(prompt)

    # fallback safety
    try:
        return json.loads(response)
    except Exception:
        return [
            "Understand the system request",
            "Identify requirements and assumptions",
            "Design system architecture and components",
            "Define data model and APIs",
            "Discuss scalability, security, and tradeoffs",
            "Finalize and structure the report"
        ]