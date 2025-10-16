from typing import TypedDict, Annotated, List, Sequence
from pydantic import BaseModel, Field
from langchain.schema import HumanMessage, AIMessage

class TestGenState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], "The messages in the conversation"]
    query: Annotated[str, "A user query containing instructions for the creation of the test case"]
    actions: Annotated[List[str], "List of actions for which to generate the code."]
    target_url: Annotated[str, "Valid URL of the website to test."]
    current_action: Annotated[int, "The index of the current action to generate the code for."]
    current_action_code: Annotated[int, "Code for the current action."]
    aggregated_raw_actions: Annotated[str, "Raw aggregation of the actions"]
    script: Annotated[str, "The generated Playwright script."]
    website_state: Annotated[str, "DOM state of the website."]
    error_message: Annotated[str, "Message that occurred during the processing of the action."]
    minimal_dom: Annotated[str, "Relevant DOM snippet for current action"]
    test_evaluation_output: Annotated[str, "Evaluation of the final test script."]
    test_name: Annotated[str, "Name of the generated test."]
    template_pw_script: Annotated[str, "Playwright script to obtain the DOM state."]

class ActionList(BaseModel):
    actions: List[str] = Field(..., description="List of atomic actions for end-to-end testing")
