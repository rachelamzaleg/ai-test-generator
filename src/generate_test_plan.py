import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage


from typing import TypedDict, List
import pandas as pd
from pydantic import BaseModel, Field


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env")

# AI Prompt using LangChain PromptTemplate
LLM_SYSTEM_PROMPT = """
Role Definition:
You are a an expert Software QA Leader with 10 years experience in saas sase environments.

QA Instructions:
Ensure all field content is precise, actionable, and professional.
Follow the schema exactly: test_case_id, test_title, description, preconditions, test_steps, test_data, expected_result, comments.
Do not add extra fields or text outside the schema.

Requirement Context:
You will be provided with a user story that outlines specific software requirements.
I want you to analyze the user story in depth and generate a comprehensive, professional set of test cases, including E2E functional steps, edge, and boundary cases, to ensure complete test coverage for the full requirements defined in the user story.
generate set of test cases to cover all aspects of the user story, covering the following tests levels as much as you can:
- Sanity test cases - cover acceptance tests
- Functional test cases - cover main E2E functionality
- Boundary test cases - cover edge limits
- Negative test cases - cover invalid inputs and error handling
"""

class TestCase(BaseModel):
    test_case_id: int = Field(..., description="Unique identifier for the test case.")
    test_title: str = Field(..., description="Title of the test case.")
    description: str = Field(..., description="Detailed description of what the test case covers.")
    preconditions: str = Field(..., description="Any setup required before execution.")
    test_steps: str = Field(..., description="Step-by-step execution guide.")
    test_data: str = Field(..., description="Input values required for the test.")
    expected_result: str = Field(..., description="The anticipated outcome.")
    comments: str = Field(..., description="Additional notes or observations.")

class TestPlan(BaseModel):
    test_cases: List[TestCase]

# Wrap LLM with structured output
structured_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=GROQ_API_KEY
)
llm_with_structured_output = structured_llm.with_structured_output(TestPlan)

class TestGenState(TypedDict):
    requirement: str
    test_plan: List[dict]

def parse_requirement(state: TestGenState) -> TestGenState:
    """
    Node: Parse Requirement
    Purpose: Prepare the requirement text for the LLM.
    Input: state['requirement'] (string)
    Output: state['requirement'] (string)
    """
    with open("..\\data\\requirements.txt", "r") as f:
        state["requirement"] = f.read()
    return state

def generate_test_cases(state: TestGenState) -> TestGenState:
    """Generate structured test cases directly from requirement text."""
    messages = [
    SystemMessage(content=LLM_SYSTEM_PROMPT),
    HumanMessage(content=state["requirement"])
]
    resp = llm_with_structured_output.invoke(messages) 
    print(resp)
    # resp is already a TestPlan object
    state["test_plan"] = [tc.dict() for tc in resp.test_cases]
    return state


def export_tests(state: TestGenState, file_path="test_cases.csv") -> TestGenState:
    """Node: Export all tests to CSV and display DataFrame."""
    df = pd.DataFrame(state.get("test_plan", []))
    df.to_csv(file_path, index=False)
    state["exported_file"] = file_path
    return state

workflow = StateGraph(TestGenState)
workflow.add_node("parse", parse_requirement)
workflow.add_node("generate_tests", generate_test_cases)
workflow.add_node("export", export_tests)

workflow.set_entry_point("parse")

# Normal flow
workflow.add_edge("parse", "generate_tests")
workflow.add_edge("generate_tests", "export")


workflow.add_edge("export", END)

app = workflow.compile()


if __name__ == "__main__":
    result = app.invoke({})


