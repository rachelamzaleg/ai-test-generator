from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from models import ActionList, TestGenState
import config
llm = config.llm


async def convert_user_instruction_to_actions(state: TestGenState) -> TestGenState:
    "Parse user instructions into a list of actions to be executed."

    output_parser = PydanticOutputParser(pydantic_object=ActionList)

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
                You are an end-to-end testing specialist.
                Your goal is to break down general business end-to-end testing tasks into smaller well-defined actions.
                These actions will be later used to write the actual code that will execute the tests.
                """
            ),
            HumanMessagePromptTemplate.from_template(
                """
                Convert the following <Input> into a JSON dictionary with the key "actions" and a list of atomic steps as its value.
                These steps will later be used to generate end-to-end test scripts.
                Each action should be a clear, atomic step that can be translated into code.
                Aim to generate the minimum number of actions needed to accomplish what the user intends to test.
                The first action must always be navigating to the target URL.
                The last action should always be asserting the expected outcome of the test.
                Do not add any extra characters, comments, or explanations outside of this JSON structure. Only output the JSON result.

                Examples:
                Input: "Test the login flow of the website"
                Output: {{
                    "actions": [
                        "Navigate to the search page via the URL.",
                        "Enter the search term for example 'LangChain' in the 'Search' input field.",
                        "Click the 'Search' button to submit the query.",
                        "Verify that the search results contain the term 'LangChain'."
                    ]
                }}

                Input: "Test adding item to the shopping cart."
                Output: {{
                    "actions": [
                        "Navigate to the product listing page via the URL.",
                        "Click on the first product in the listing to open product details",
                        "Click the 'Add to Cart' button to add the selected item",
                        "Expect the selected item name appears in the shopping cart sidebar or page"
                    ]
                }}

                <Inptut>: {query}
                <Output>:
                """
            ),
        ]
    )

    chain = chat_template | llm | output_parser

    actions_structure = chain.invoke({"query": state["query"]})
    state["actions"]=actions_structure.actions
    print(state["actions"])
    return state