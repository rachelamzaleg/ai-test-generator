import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import pandas as pd

# MAX_RETRIES = 3


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env")

# Init LLM
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)



class TestGenState(TypedDict):
    requirement: str
    sanity: List[str]
    regression: List[str]
    detailed: List[str]
    all_tests: List[dict]
    attempt: int

def init_state(state: TestGenState) -> TestGenState:
    return {
        "sanity": [],
        "regression": [],
        "detailed": [],
        "all_tests": [],
        "attempt": 0
    }
def parse_requirement(state: TestGenState) -> TestGenState:
    """
    Node: Parse Requirement
    Purpose: Prepare the requirement text for the LLM.
    Input: state['requirement'] (string)
    Output: state['requirement'] (string)
    """
    
    return {"requirement": state["requirement"]}




def generate_sanity_tests(state: TestGenState) -> TestGenState:
    """Node: Generate sanity-level test steps (acceptance test).
    Purpose: Use LLM to generate structured sanity-level test steps (acceptance test)test cases for a requirement.
    Input: state['requirement'] (string)
    Output: state['sanity'] (list of test cases with fields: id, description, steps, expected, type)
    """
    
    prompt = f"""Generate 3 sanity test cases for the requirement:
    {state['requirement']}
    Only include basic verification steps.
    Each test case must include the following fields:
    - id
    - description
    - steps
    - expected
    - type (sanity)
    """
    resp = llm.invoke(prompt)
    steps = [s.strip() for s in resp.content.split("\n") if s.strip()]
    state["sanity"] = steps
    return state

def generate_regression_tests(state: TestGenState) -> TestGenState:
    """Node: Generate regression-level test steps (deep E2E).
    Purpose: Use LLM to generate structured regression-level test steps (deep E2E) test cases for a requirement.
    Input: state['requirement'] (string)
    Output: state['regression'] (list of test cases with fields: id, description, steps, expected, type)
    """

    prompt = f"""Generate 3 regression test cases for the requirement:
    {state['requirement']}
    Cover full end-to-end flows.
    Only include basic verification steps.
    Each test case must include the following fields:
    - id
    - description
    - steps
    - expected
    - type (regression)
    """
    resp = llm.invoke(prompt)
    steps = [s.strip() for s in resp.content.split("\n") if s.strip()]
    state["regression"] = steps
    return state


def generate_detailed_tests(state: TestGenState) -> TestGenState:
    """Node: Generate detailed test steps (edge cases / complex flows).
    Purpose: Use LLM to generate structured detailed test steps (edge cases and complex tests) test cases for a requirement.
    Input: state['requirement'] (string)
    Output: state['detailed'] (list of test cases with fields: id, description, steps, expected, type)
    """
    prompt = f"""
    Generate 3 detailed test steps for the requirement:
    {state['requirement']}
    Include edge cases, complex flows, and boundary conditions.
    Only include basic verification steps.
    Each test case must include the following fields:
    - id
    - description
    - steps
    - expected
    - type (detailed)
    """
    resp = llm.invoke(prompt)
    steps = [s.strip() for s in resp.content.split("\n") if s.strip()]
    state["detailed"] = steps
    return state

def merge_tests(state: TestGenState) -> TestGenState:
    """Node: Merge all test types into a single list of dicts."""
    all_tests = []
    for t_type in ["sanity", "regression", "detailed"]:
        for step in state.get(t_type, []):
            all_tests.append({"type": t_type, "step": step})
    state["all_tests"] = all_tests
    return state

def export_tests(state: TestGenState, file_path="test_cases.csv") -> TestGenState:
    """Node: Export all tests to CSV and display DataFrame."""
    df = pd.DataFrame(state.get("all_tests", []))
    df.to_csv(file_path, index=False)
    state["exported_file"] = file_path
    return state

'''
def is_retry_needed(state: TestGenState) -> str:
    """Return continue if JSON invalid and attempts < MAX_RETRIES."""
    valid = True
    
    state["valid"] = valid
    if not valid and state["attempt"] < MAX_RETRIES:
        return  "continue"
    return "end"
'''

workflow = StateGraph(TestGenState)
workflow.add_node("init", init_state)
workflow.add_node("parse", parse_requirement)
workflow.add_node("generate_sanity", generate_sanity_tests)
workflow.add_node("generate_regression", generate_regression_tests)
workflow.add_node("generate_detailed", generate_detailed_tests)
workflow.add_node("merge", merge_tests)
workflow.add_node("export", export_tests)

workflow.set_entry_point("init")

# Normal flow
workflow.add_edge("init", "parse")
workflow.add_edge("parse", "generate_sanity")
workflow.add_edge("generate_sanity", "generate_regression")
workflow.add_edge("generate_regression", "generate_detailed")
workflow.add_edge("generate_detailed", "merge")
workflow.add_edge("merge", "export")
workflow.add_edge("export", END)

# Retry flow
'''
workflow.add_conditional_edges('generate_sanity', #Source Node
is_retry_needed, #Action
  {
    'continue': 'generate_regression',
    'end': END
})
'''

app = workflow.compile()


if __name__ == "__main__":
    result = app.invoke({"requirement": "The system should allow login with username/password"})
    print(result["all_tests"])



