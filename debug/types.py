from typing import TypedDict, Dict, Union, List, Any

MessageDict = Dict[str, str]

OpenAIObject = Dict[str, Union[
    str, 
    int, 
    float, 
    List[Dict[str, Union[str, int, float, Dict[str, Any]]]]
]]

class SystemMessage(TypedDict):
    content: str
    role: str

class TranscriptDict(TypedDict):
    user_message: str
    assistant_message: str
