import json

from pydantic import BaseModel  # this is the standard class


# Taking for example the last LLM response, I want this structure:
# {tool_name: 'tool_browser',
#  tool_input: {'q':'September 9 2024 deaths'},
#  tool_output: str( tool_browser({'q':'September 9 2024 deaths'})) }

class MyAgentRes(BaseModel):
    tool_name: str  # <--must be a string = 'tool_browser'
    tool_input: dict  # <--must be a dictionary = {'q':'September 9 2024 deaths'}
    tool_output: str | None = None  # can be a string or None, default = None

    @classmethod
    def from_llm(cls, res: dict):  # <--return the class itself
        try:
            out = json.loads(res["message"]["content"])
            return cls(tool_name=out["name"], tool_input=out["parameters"])
        except Exception as e:
            print(f"Error from Ollama:\n{res}\n")
            raise e
