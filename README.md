
# Autonomous AI Agent System Design Generator
A **Python-based Autonomous AI Agent** using **FastAPI** that:

* Accepts a natural language request through `POST /agent`
* Autonomously determines the tasks required
* Creates its own execution plan
* Executes the plan using an LLM
* Generates a professional **Microsoft Word (.docx)** document
* Returns both the execution plan and the generated document path

The focus is **autonomous planning**, modular engineering, and clean software architecture rather than UI.

---

# Final Use Case

The agent generates a **System Design Report**.

Example requests:
* Design a scalable chat system
* Design a URL shortener
* Design a ride-sharing application
* Explain Netflix architecture
* Design an Event Ticket Booking System

The generated Word document is a structured **System Design Report**, which qualifies as a structured business document because companies regularly create such documents for architecture reviews, design discussions, technical proposals, and engineering planning.

# Why this is useful in business
Possible business use cases:

* Engineering teams creating architecture proposals
* Software consultants preparing design documents
* Technical leads documenting new systems
* Solution architects producing design reports
* Internal documentation
* Client architecture presentations

This is much more realistic than simply asking ChatGPT to answer a question.
---

# Agent Architecture
We intentionally chose a **single autonomous agent** instead of a multi-agent system because:

* Simpler
* Easier to explain
* Easier to maintain

Workflow:

```
User

↓

FastAPI

↓

Orchestrator

↓

Planner

↓

Execution Plan

↓

Executor

↓

LLM

↓

Word Document Generator

↓

Response
```

---

# Project Structure

```
AI_Agent/

│

├── main.py
├── models.py
├── .env
├── requirements.txt

│

├── agent/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── planner.py
│   └── executor.py

│

├── tools/
│   ├── __init__.py
│   ├── llm.py
│   └── doc_generator.py

│

└── output/
```

The planner prompt is now inside `planner.py` because there is only one planning prompt. Keeping it there reduces unnecessary files while maintaining modularity.

---

# Responsibilities of Each File

## main.py

Only handles HTTP requests.

Responsibilities:

* FastAPI initialization
* API endpoints
* Request validation
* Calls the orchestrator

No AI logic.

---

## models.py

Contains Pydantic models.

```
AgentRequest

AgentResponse
```

Used for request validation.

---

## orchestrator.py

Coordinates the workflow.

Responsibilities:

* Call planner
* Call executor
* Call document generator
* Return final response

It does **not** perform AI generation.

---

## planner.py

Responsible only for planning.

Uses Gemini to generate an execution plan.

Returns a JSON list such as:

```json
[
    "Understand the problem",
    "Identify requirements",
    "Design architecture",
    "Design database",
    "Discuss scalability",
    "Discuss tradeoffs",
    "Write conclusion"
]
```

It includes fallback logic if JSON parsing fails.

---

## executor.py

Responsible only for executing the plan.

Current implementation loops through each planning step.

For every step:

* Sends prompt to Gemini
* Generates that report section
* Stores the generated content

Returns a dictionary of report sections.

---

## doc_generator.py

Responsible only for creating the Word document.

Uses:

```
python-docx
```

Creates:

```
output/report.docx
```

Returns the file path.

---

## llm.py

Responsible only for communicating with Gemini.

Current implementation:

* Loads API key from `.env`
* Calls Gemini
* Returns generated text

This file is also the correct place to implement retry logic.

---

# FastAPI Endpoints

```
GET /
```

Returns

```json
{
    "status":"running",
    "message":"Agent is ready"
}
```

---

```
POST /agent
```

Accepts

```json
{
    "request":"Design a scalable URL shortener"
}
```

Returns

```json
{
    "status":"success",
    "execution_plan":[...],
    "document_path":"output/report.docx",
    "message":"Report generated successfully."
}
```

---

# Technologies Chosen

### FastAPI

Chosen because:

* Fast
* Lightweight
* Automatic Swagger documentation
* Request validation
* Industry standard for Python APIs

---

### Gemini Free API

Chosen because:

* Free tier
* No local model installation
* Easy integration
* Good reasoning capability

Current model:

```
gemini-2.5-flash
```

---

### python-docx

Used to generate Word documents.

---

### Pydantic

Used for request validation.

---

# Engineering Improvement

We chose:

## Retry & Fallback Logic

Implemented inside:

```
tools/llm.py
```

Instead of the planner handling retries, the LLM client itself performs retries on temporary failures (e.g., HTTP 429 rate limits). This centralizes resilience in one place so every component that uses the LLM benefits.

---

# Problem Encountered

Gemini returned:

```
429 RESOURCE_EXHAUSTED
```

Reason:

The planner made one LLM call, then the executor made one LLM call **per planning step**.

For example:

```
Planner

↓

1 API call

↓

Executor

↓

7 more API calls
```

One request could consume around 8 API calls, quickly exhausting the free-tier quota.

---

# Planned Improvement

Reduce the number of Gemini calls.

Instead of generating one report section per LLM call:

```
Architecture

↓

Database

↓

Security

↓

Tradeoffs
```
