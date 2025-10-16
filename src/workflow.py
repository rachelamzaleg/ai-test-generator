from models import TestGenState
from llm_integration import convert_user_instruction_to_actions

from build_selenium_script import (
    selenium_template,
    execute_test_case,
    post_process_script
)
from dom_parser import  get_website_dom
from langgraph.graph import StateGraph, END

async def run_workflow(query: str, target_url: str):
    """Run the LangGraph workflow"""
    initial_state = {
        'messages': [],
        'query': query,
        'actions': [],
        'target_url': target_url,
        'current_action': 0,
        'current_action_code': "",
        'aggregated_raw_actions': "",
        'script': None,
        'website_state': None,
        'minimal_dom': None,
        'error_message': None,
        'test_name': None,
        'dom_script': None,
        
    }

    result = await app.ainvoke(initial_state)

    return result

workflow = StateGraph(TestGenState)
workflow.add_node("convertor", convert_user_instruction_to_actions)
workflow.add_node("template", selenium_template)

'''workflow.add_node("get_state", get_website_dom)
workflow.add_node("generate_code", generate_code_for_action)
workflow.add_node("validate", validate_generated_action)'''
workflow.add_node("post_process", post_process_script)
workflow.add_node("execute_test", execute_test_case)

workflow.set_entry_point("convertor")

workflow.add_edge("convertor", "template")
'''workflow.add_edge("template", "get_state")
#workflow.add_edge("initializer", "get_state")
workflow.add_edge("get_state", "generate_code")
workflow.add_edge("generate_code", "validate")'''
#workflow.add_edge("validate", "post_process")
workflow.add_edge("template", "post_process")
workflow.add_edge("post_process", "execute_test")
workflow.add_edge("execute_test", END)


app = workflow.compile()
