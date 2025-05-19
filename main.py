import ollama
from pprint import pprint
import json

from AgentRes import MyAgentRes
from State import State
from agent import run_agent
from settings import llm, prompt
from tools import prompt_tools, browser, dict_tools

# print(res)

# @tool("tool_browser")
# def tool_browser(q: str) -> str:
#     """Search on DuckDuckGo browser by passing the input `q`"""
#     return DuckDuckGoSearchRun().run(q)

# test
# print(tool_browser(q))

# @tool("final_answer")
# def final_answer(text:str) -> str:
#     """Returns a natural language response to the user by passing the input `text`.
#     You should provide as much context as possible and specify the source of the information.
#     """
#     return text

# print(final_answer)
# print(tool_browser.get('function'))
# print([v.type for n,v in enumerate(dic_tools.values())])


q = '''who died on September 9, 2024?'''

llm_res = ollama.chat(model=llm,
                messages=[{"role": "system", "content": prompt+"\n"+prompt_tools},
                          {"role": "user", "content":q}], format="json")

# res["message"]["content"]
print("\nllm output:\n", llm_res["message"]["content"])
tool_input = json.loads(llm_res["message"]["content"])["parameters"]["q"]
print("\n", tool_input)

context = browser(tool_input)
print("\ntool output:\n", context)

llm_output = ollama.chat(
    model=llm,
    messages=[{"role":"system", "content":"Give the most accurate answer using the following information:\n"+context},
              {"role":"user", "content":q}
             ])

print("\nllm output:\n", llm_output["message"]["content"])

# test
# agent_res = MyAgentRes.from_llm(llm_res)
# print("from\n", llm_res["message"]["content"], "\nto")
# pprint(agent_res)
# print("\nOr \n")
# pprint(MyAgentRes(tool_name = "tool_browser",
#          tool_input = {'q':'September 9 2024 deaths'},
#          tool_output = str( browser('September 9 2024 deaths')) ))

history=[{"role": "user", "content": "hi there, how are you?"},
         {"role": "assistant", "content": "I'm good, thanks!"},
         {"role": "user", "content": "I have a question"},
         {"role": "assistant", "content": "tell me"}]

# test agent
agent_res = run_agent(user_q=q, chat_history=history, lst_res=[], lst_tools=dict_tools.keys())
# print("\nagent_res:", agent_res)

state = State({"user_q": q, "chat_history":history, "lst_res":[agent_res], "output": {}})
pprint(state)

# Agent
def node_agent(state):
    print("--- node_agent ---")
    agent_res = run_agent(lst_tools={k:v for k,v in dict_tools.items() if k in ["tool_browser","final_answer"]},
                          user_q=state["user_q"],
                          chat_history=state["chat_history"],
                          lst_res=state["lst_res"])
    # print("\nagent_res:", agent_res)
    return {"lst_res":[agent_res]} #<--must return the list of agent_res

# test
pprint(node_agent(state))


def node_tool(state):
    print("--- node_tool ---")
    res = state["lst_res"][-1]
    print(f"{res.tool_name}(input={res.tool_input})")

    agent_res = MyAgentRes(tool_name=res.tool_name,
                         tool_input=res.tool_input,
                         tool_output=str(dict_tools[res.tool_name](res.tool_input)))

    return {"output": agent_res} if res.tool_name == "final_answer" else {"lst_res": [agent_res]}


# test
node_tool(state)
