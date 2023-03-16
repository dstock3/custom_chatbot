#from systemStatus.get_system_data import get_system_data
from system.email_checker import check_emails

custom_commands = {
    "check my system": {
        "interpret": "true",
        #"function": get_system_data,
        "prompt": "Analyze this system data: "
    },
    "check emails": {
        "interpret": "true",
        "function": check_emails,
        "prompt": "Check these emails and summarize them for me. Be sure to let me know if there's anything super important. "
    },
}
