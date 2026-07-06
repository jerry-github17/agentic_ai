from agent.planner import create_plan
from agent.executor import execute_plan
from agent.reflection import reflect
from tools.doc_generator import generate_doc
import logging

logger = logging.getLogger()

def run_agent(user_request: str):
    print("========== AI AGENT ==========", flush=True)
    print("Received request:", user_request, flush=True)

    plan = create_plan(user_request)
    logger.info("Planning completed.")
    

    sections = execute_plan(user_request, plan)
    logger.info("Execution completed.")
    review = reflect(user_request, sections)
    file_path = generate_doc(sections, review)
    logger.info("Document generated: %s", file_path)

    logger.info("Agent task completed successfully.")

    return{
        "status":"success",
        "plan":plan,
        "document":file_path,
        "execution_plan": plan,
        "reflection": reflect,
        "message": "Task finished successfully.",
    }

