from models import TestGenState
import pytest
import re
import io
import ast
from contextlib import redirect_stderr, redirect_stdout

from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
import config


llm = config.llm


async def selenium_template(state: TestGenState) -> TestGenState:
    """Initialize a Selenium script with the first action — navigate and capture DOM."""
    selenium_code = f"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def launch_browser():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def navigate_to(driver, url: str):
    driver.get(url)

def get_dom_state(driver):
    return driver.page_source

def close_browser(driver):
    driver.quit()

def get_page_dom():
    driver = launch_browser()
    try:
        navigate_to(driver, "{state['target_url']}")
        dom_state = get_dom_state(driver)
        return dom_state
    finally:
        close_browser(driver)

def open_browser_and_navigate():
    driver = launch_browser()
    navigate_to(driver, "{state['target_url']}")
    return driver

# Next Actions
"""
    state["script"] = selenium_code
    return state


async def build_initial_action(state: TestGenState) -> TestGenState:
    """Initialize Selenium script with first navigation action."""
    initial_script = f"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def generated_script_run():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Action 0
    driver.get("{state['target_url']}")

    # Next Action

    # Always return driver at the end
    return driver
"""
    state["script"] = initial_script
    state["current_action"] = int(state["current_action"]) + 1
    return state


async def generate_code_for_action(state: TestGenState) -> TestGenState:
    """Generate Selenium code for the current action."""
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("""
        You are an end-to-end testing specialist. Your goal is to write a Python Selenium code
        for an action specified by the user.
        """),
        HumanMessagePromptTemplate.from_template("""
        You will be provided with a minimal website <DOM>, the <Previous Actions> (not to include in output),
        and the <Action> for which to write a Python Selenium code.
        This <Action> code will be inserted into an existing Selenium script. Therefore, the code should be atomic.
        Assume the variable 'driver' is available.
        Use data-testid for locating elements when possible, otherwise use a suitable selector.
        Always include any waits or assertions as appropriate.
        {last_action_assertion}

        ---
        <Previous Actions>:
        {previous_actions}
        ---
        <Action>:
        {action}
        ---
        ### UNTRUSTED CONTENT DELIMITER ###
        <DOM>:
        {minimal_dom}
        """)
    ])

    print(f"Generating action number: {state['current_action']}, {state['actions'][state['current_action']]}")

    chain = chat_template | llm
    current_action = state["actions"][state["current_action"]]
    last_action_assertion = "Add an assertion to verify success for this final action." \
        if state["current_action"] == len(state["actions"]) - 1 else ""

    current_action_code = chain.invoke({
        "action": current_action,
        "minimal_dom": state["minimal_dom"],
        "previous_actions": state["aggregated_raw_actions"],
        "last_action_assertion": last_action_assertion
    }).content

    state["current_action_code"] = current_action_code
    print("Generated Action Code:\n", current_action_code)
    return state


async def validate_generated_action(state: TestGenState) -> TestGenState:
    """Validate and insert generated action code into the script."""
    current_action_code = state["current_action_code"]
    current_action = state["current_action"]
    script = state["script"]

    print(f"Validating action number {current_action}")

    try:
        ast.parse(current_action_code)
    except SyntaxError as e:
        state["error_message"] = f"Invalid Python code: {e}"
        return state

    if "driver." not in current_action_code:
        state["error_message"] = "No Selenium driver command found in current_action_code."
        return state

    indentation = "    " * 1
    indented_code = "\n".join([indentation + line for line in current_action_code.split("\n")])
    indented_code += f'\n{indentation}driver.save_screenshot("screenshot_action_{current_action}.png")'

    code_to_insert = f"# Action {current_action}\n{indented_code}\n{indentation}# Next Action"
    updated_script = re.sub(r'# Next Action', code_to_insert, script, count=1)

    state["script"] = updated_script
    state["current_action"] = current_action + 1
    state["aggregated_raw_actions"] += "\n" + current_action_code

    print("Updated Script:\n", state["script"])
    return state


async def post_process_script(state: TestGenState) -> TestGenState:
    """Finalize the Selenium code into a Pytest test case."""
    final_script = re.sub(r'# Next Action.*', '', state["script"], flags=re.DOTALL)

    global_helpers = """
def take_global_screenshot(driver):
    driver.save_screenshot("global_screenshot.png")

def global_assertion_hook(driver):
    # Example global verification
    assert driver.title != "", "Page title is empty"
"""

    # Generate test name via LLM
    chat_template = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template("""
        You are generating a short Python test function name in snake_case.
Constraints:
- Maximum length: 10 characters (excluding the 'test_' prefix).
- Use only lowercase letters, numbers, and underscores.
- Keep it short, descriptive, and deterministic.
- Do NOT include extra words like "verify", "should", or "results_appear".
- Output ONLY the name (no explanations, no code, no prefix).

Context:
User query: {query}
Actions summary: {actions}

Return ONLY the short name (e.g., "login_ok", "cart_add", "nav_home").
""")
    ])

    chain = chat_template | llm
    test_name = chain.invoke({
        "query": state["query"],
        "actions": state["aggregated_raw_actions"]
    }).content
    test_name = f'test_{re.sub(r"[^\w]", "_", test_name.strip())}'

    test_script = f"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

{final_script}

{global_helpers}

@pytest.mark.parametrize("driver", [open_browser_and_navigate()], indirect=False)
def {test_name}(driver):
    # Next Action

    # Global verification
    take_global_screenshot(driver)
    global_assertion_hook(driver)
    driver.quit()
"""
    state["script"] = test_script
    state["test_name"] = test_name
    print("Generated Test Name:", test_name)
    print("Final Selenium Test Script:\n", test_script)
    return state


def execute_test_case(state: TestGenState) -> TestGenState:
    """Execute the generated Selenium test."""
    print("Evaluating the generated test with PyTest.")
    test_file = "generated_test.py"
    with open(test_file, "w") as f:
        f.write(state["script"])

    output = io.StringIO()
    with redirect_stdout(output), redirect_stderr(output):
        pytest.main(["-v", test_file])
    state["test_evaluation_output"] = output.getvalue()
    print("Test Evaluation Output:\n", state["test_evaluation_output"])
    return state
