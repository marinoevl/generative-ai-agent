'''
Messages in Memory will have this structure:
[{'role':'assistant', 'content':'{"name":"final_answer", "parameters":{"text":"How can I assist you today?"}}'},
 {'role':'user', 'content':None}]
'''
import json

from AgentRes import MyAgentRes


def save_memory(lst_res:list[MyAgentRes], user_q:str):
    ## create
    memory = []
    for res in [res for res in lst_res if res.tool_output is not None]:
        memory.extend([
            ### assistant message
            {
                "role": "assistant",
                "content":json.dumps({"name":res.tool_name, "parameters":res.tool_input}),
            },
            ### user message
            { "role": "user", "content":res.tool_output }
        ])

    ## add a reminder of the original goal
    if memory:
        memory += [
            {
                "role":"user",
                "content":(f'''
                This is just a reminder that my original query was `{user_q}`.
                Only answer to the original query, and nothing else, but use the information I gave you.
                Provide as much information as possible when you use the `final_answer` tool.
                ''')
            }
        ]
    return memory