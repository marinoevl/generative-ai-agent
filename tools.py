from langchain_community.tools import DuckDuckGoSearchRun
from semantic_router.utils.function_call import FunctionSchema


def browser(question: str) -> str:
    """Search on DuckDuckGo browser by passing the input `q`"""
    return DuckDuckGoSearchRun().run(question)

def answer(text:str) -> str:
    """Returns a natural language response to the user by passing the input `text`.
    You should provide as much context as possible and specify the source of the information.
    """
    return text

tool_browser = FunctionSchema(browser).to_ollama()
final_answer = FunctionSchema(answer).to_ollama()

dict_tools = {"tool_browser":tool_browser,
             "final_answer":final_answer}

str_tools = "\n".join([str(n+1)+". `"+str(v.get('function').get('name'))+"`: "+str(v.get('function').get('description')) for n,v in enumerate(dict_tools.values())])

prompt_tools = f"You can use the following tools:\n{str_tools}"