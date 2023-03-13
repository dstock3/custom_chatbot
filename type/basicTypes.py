from typing import Dict, Any, Optional

def checkInstance(argument, expected_type):
    if not isinstance(argument, expected_type):
        raise TypeError('The ' + str(argument) + ' argument must be a ' + str(expected_type) + ' value.')

IsAudio = bool
Input = Optional[str]
ChatTranscript = Dict[str, Any]
