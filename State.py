import typing

from AgentRes import MyAgentRes


class State(typing.TypedDict):
    user_q: str
    chat_history: list
    lst_res:list[MyAgentRes]
    output: dict