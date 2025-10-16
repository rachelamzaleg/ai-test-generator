

from models import TestGenState
from bs4 import BeautifulSoup



def extract_relevant_dom_helper(full_dom: str, action: str, max_nodes: int = 50) -> str:
    """
    Extract a minimal DOM snippet relevant to the current action.
    Generic rules:
        - If action involves clicking, take buttons and links.
        - If action involves typing/filling, take input fields.
        - If action involves asserting/verifying, take visible text elements.
        - Otherwise, take top interactive elements.
    """
    soup = BeautifulSoup(full_dom, "html.parser")
    elements = []

    action_lower = action.lower()
    if "click" in action_lower:
        elements = soup.find_all(["button", "a"], limit=max_nodes)
    elif "input" in action_lower or "type" in action_lower or "enter" in action_lower:
        elements = soup.find_all("input", limit=max_nodes)
    elif "assert" in action_lower or "verify" in action_lower or "expect" in action_lower:
        elements = soup.find_all(text=True, limit=max_nodes)
    else:
        elements = soup.find_all(["input", "button", "a"], limit=max_nodes)

    minimal_dom = "".join(str(el) for el in elements)
    return minimal_dom

async def get_website_dom(state: TestGenState) -> TestGenState:
    """
    Get the full DOM and extract the minimal DOM relevant for the current action.
    - website_state: full DOM
    - minimal_dom: relevant snippet for the current action
    """
    print(f"Obtaining DOM for action number {state['current_action']}")

    exec_namespace = {}
    exec(state["script"], exec_namespace)

    # Run the script to get full DOM
    full_dom = await exec_namespace["get_page_dom"]()
    state["website_state"] = full_dom

    # Extract minimal DOM for the current action
    current_action = state["actions"][state["current_action"]]
    state["minimal_dom"] = extract_relevant_dom_helper(full_dom, current_action)

    return state