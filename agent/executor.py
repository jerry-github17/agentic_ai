from tools.llm import call_llm
import json

def execute_plan(request: str, plan :list):
        prompt = f"""
You are a senior Software Architect writing a SYSTEM DESIGN REPORT.

User Request:
{request}

Execution Plan:
{plan}

STRICT INSTRUCTIONS:
- Follow the execution plan
- Generate a complete professional system design report
- Use structured numbered sections

Return ONLY valid JSON in this EXACT structure:

{{
  "1. System Overview": "...",
  "2. Functional Requirements": "...",
  "3. Non-Functional Requirements": "...",
  "4. High-Level Architecture": "...",
  "5. API Design": "...",
  "6. Database Design": "...",
  "7. Scalability Considerations": "...",
  "8. Security Considerations": "...",
  "9. Trade-offs": "...",
  "10. Risks & Design Gaps": "...",
  "11. Recommendations": "..."
}}

Rules:
- No markdown
- No explanations
- No extra text

"""
        response = call_llm(prompt)
        try:
                return json.loads(response)
        except json.JSONDecodeError:
                return{ 
                        "Generated Report": response      
                }