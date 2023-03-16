from system.system_status import get_system_data, get_network_data
from system.weather import get_weather
from system.email_checker import check_emails

custom_commands = {
    "check my system": {
        "interpret": "true",
        "function": get_system_data,
        "prompt": "Analyze this system data and brief me on its status: "
    },
    "check my network": {
        "interpret": "true",
        "function": get_network_data,
        "prompt": "Analyze the network data on my system and summarize it for me in a concise manner: "
    },
    "check my email": {
        "interpret": "true",
        "function": check_emails,
        "prompt": "Check these emails and summarize them in a concise manner for me. Be sure to let me know if there's anything important."
    },
    "check the weather": {
        "interpret": "true",
        "function": get_weather,
        "prompt": "Get the current weather for this location and provide me with a summary: "
    }
}
