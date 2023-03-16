from system.system_status import get_system_data, get_disk_usage, get_network_data, get_memory_intensive_processes, get_cpu_intensive_processes
from system.weather import get_weather
from system.email_checker import check_emails

custom_commands = {
    "check my system": {
        "interpret": "true",
        "function": get_system_data,
        "prompt": "Analyze this system data and brief me on its status: ",
        "alt": 
            ["check my system status", "check my system data", "check my system information", "check my system info", "check my system stats", "check my system statistics", "check my system metrics", "check my system health"]
    },
    "check my disk usage": {
        "interpret": "true",
        "function": get_disk_usage,
        "prompt": "Analyze the disk usage on this system and summarize it for me in a concise manner: ",
        "alt": ["check my disk usage", "check my disk data", "check my disk information", "check my disk info", "check my disk stats", "check my disk statistics", "check my disk metrics", "check my disk health"]
    },
    "check my network": {
        "interpret": "true",
        "function": get_network_data,
        "prompt": "Analyze the network data on my system and summarize it for me in a concise manner: ",
        "alt": ["check network status", "check network data", "check network information", "check network info", "check network stats", "check network statistics", "check network metrics", "check network health"]
    },
    "check my processes and sort by memory usage": {  
        "interpret": "true",
        "function": get_memory_intensive_processes,
        "prompt": "Analyze the running processes on my system and summarize them for me in a concise manner. Also check for any suspicious processes. ",
        "alt": ["what are the memory intensive processes", "check for memory intensive processes"]
    },
    "check my processes and sort by cpu usage": {  
        "interpret": "true",
        "function": get_cpu_intensive_processes,
        "prompt": "Analyze the running processes on my system and summarize them for me in a concise manner. Also check for any suspicious processes. ",
        "alt": ["what are the cpu intensive processes", "check for cpu intensive processes"]
    },
    "check my email": {
        "interpret": "true",
        "function": check_emails,
        "prompt": "Check these emails and summarize them in a concise manner for me. Be sure to let me know if there's anything important.",
        "alt": ["check my emails", "check my inbox", "check my email inbox", "check my email account", "check my email accounts", "check email", "check emails", "check inbox", "check email inbox", "check email account", "check email accounts"]
    },
    "check the weather": {
        "interpret": "true",
        "function": get_weather,
        "prompt": "Get the current weather for this location and provide me with a summary: ",
        "alt": ["get weather data", "whats the weather", "check weather", "get weather data", "hows the weather"]
    }
}
