from pprint import pprint

import ollama

from AgentRes import MyAgentRes
from memory_system import save_memory
from settings import prompt, llm
from tools import prompt_tools


def run_agent(user_q:str, chat_history:list[dict], lst_res:list[MyAgentRes], lst_tools:list) -> MyAgentRes:
    ## start memory
    memory = save_memory(lst_res=lst_res, user_q=user_q)

    ## track used tools
    if memory:
        tools_used = [res.tool_name for res in lst_res]
        if len(tools_used) >= len(lst_tools):
            memory[-1]["content"] = "You must now use the `final_answer` tool."

    ## messages
    messages = [{"role":"system", "content":prompt+"\n"+prompt_tools},
                *chat_history,
                {"role":"user", "content":user_q},
                *memory]
    # pprint(messages) #<--print to see prompt + tools + chat_history

    ## output
    llm_res = ollama.chat(model=llm, messages=messages, format="json")
    return MyAgentRes.from_llm(llm_res)