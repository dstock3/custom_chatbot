from typing import Dict, Union, List, Any

# Define the type for a message dictionary
MessageDict = Dict[str, str]

OpenAIObject = Dict[str, Union[
    str, 
    int, 
    float, 
    List[Dict[str, Union[str, int, float, Dict[str, Any]]]]
]]
