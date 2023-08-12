from system.system_status import get_system_data, get_disk_usage, get_network_data, get_memory_intensive_processes, get_cpu_intensive_processes
from system.weather import get_weather
from system.email_checker import check_emails
from system.determineOS import get_linux_distro, determine_os
from system.news import get_news
from intel.remember import remember_when
from system.search import search_the_web

custom_commands = {
    "search": {
        "interpret": True,
        "meta": True,
        "function": search_the_web,
        "prompt": "You've been provided with search results to present to the user. Please summarize the results in a concise manner:",
        "alt": [
            "search for", "look up", "find", "search", "look for",
            "find me", "look up", "search for"
        ]
    },
    "remember when": {
        "interpret": True,
        "meta": True,
        "function": remember_when,
        "prompt": None,
        "alt": [
            "do you remember", "do you recall", "think back to", "cast your mind back", "reminisce about", "bring to mind", "think of the time", "recollect"
        ]
    },
    "check my system": {
        "interpret": True,
        "meta": False,
        "function": get_system_data,
        "prompt": "Computer, check my system. Analyze this system data and brief me on its status:",
        "alt": [
            "check my system status", "check my system data", "check my system information", "check my system info", "check my system stats", "check my system statistics", "check my system metrics", "check my system health", "analyze system performance", "evaluate system status", "system status summary", "show system details", "computer-analyzed system performance", "monitor system health", "inspect system information", "system health check", "overview of system data", "current system metrics", "assess system health", "assess system help"
        ]
    },
    "check my disk usage": {
        "interpret": True,
        "meta": False,
        "function": get_disk_usage,
        "prompt": "Computer, check my disk usage. Analyze the disk usage on this system and summarize it for me in a concise manner:",
        "alt": [
            "how much space do i have", "check my disk usage", "check my disk data", "check my disk information", "check my disk info", "check my disk stats", "check my disk statistics", "check my disk metrics", "check my disk health", "analyze disk space", "evaluate disk usage", "disk usage summary", "show disk space details", "monitor disk usage", "inspect disk usage", "available disk space", "current disk usage", "get disk usage report", "assess disk health"
        ]
    },
    "check my network": {
        "interpret": True,
        "meta": False,
        "function": get_network_data,
        "prompt": "Computer, check my Network. Analyze the network data on my system and summarize it for me in a concise manner:",
        "alt": [
            "check network status", "check network data", "check network information", "check network info", "check network stats", "check network statistics", "check network metrics", "check network health",
            "analyze network performance", "monitor my network", "get network details", "show network information", "network status report", "overview of network data", "network health check", "inspect network status", "current network metrics", "evaluate network health"
        ]
    },
    "check my processes and sort by memory usage": {
        "interpret": True,
        "meta": False,
        "function": get_memory_intensive_processes,
        "prompt": "Computer, check my processes and sort by memory usage. Analyze the running processes on my system and summarize them for me in a concise manner. Also check for any suspicious processes.",
        "alt": [
            "what are the memory intensive processes", "check for memory intensive processes",
            "list memory heavy processes", "show memory intensive tasks", "high memory usage processes", "find processes with high memory usage", "top memory consuming processes", "memory usage summary", "running processes by memory usage", "analyze memory usage by process", "processes using most memory", "monitor memory usage by processes"
        ]
    },
    "check my processes and sort by cpu usage": {
        "interpret": True,
        "meta": False,
        "function": get_cpu_intensive_processes,
        "prompt": "Computer, check my processes and sort by CPU usage. Analyze the running processes on my system and summarize them for me in a concise manner. Also check for any suspicious processes.",
        "alt": [
            "what are the cpu intensive processes", "check for cpu intensive processes",
            "list cpu heavy processes", "show cpu intensive tasks", "high cpu usage processes", "find processes with high cpu usage", "top cpu consuming processes", "cpu usage summary", "running processes by cpu usage", "analyze cpu usage by process", "processes using most cpu", "monitor cpu usage by processes", "check for CPU intensive processing"
        ]
    },
    "check my email": {
        "interpret": True,
        "meta": False,
        "function": check_emails,
        "prompt": "Computer, check my email. Check these emails and summarize them in a concise manner for me. If it's empty, let me know I don't have any new emails. Be sure to let me know if there's anything important: ",
        "alt": [
            "check my emails", "check my inbox", "check my inbox", "check my email account", "check my email accounts", "check email", "check emails", "check inbox", "check email inbox", "check email account", "check email accounts", "read my emails", "email summary", "any new emails", "update me on my emails", "summarize my emails", "email overview", "new messages in my inbox", "unread emails", "important emails", "scan my inbox", "check in box"
        ]
    },
    "check the weather": {
        "interpret": True,
        "meta": False,
        "function": get_weather,
        "prompt": "Computer, check the weather. Get the current weather for this location and provide me with a summary: ",
        "alt": [
            "get weather data", "whats the weather", "check weather", "get weather data", "hows the weather",
            "whats the weather like", "tell me the weather", "weather update", "current weather",
            "weather forecast", "weather today", "weather conditions", "give me the weather",
            "local weather", "show me the weather"
        ]
    },
    "whats my operating system": {
        "interpret": True,
        "meta": False,
        "function": determine_os,
        "prompt": "Computer, what's my operating system? Let me know that I am using: ",
        "alt": [
            "identify my operating system", "which operating system am I using", "find my OS", "determine my OS", "OS details", "get my operating system info", "reveal my OS", "what OS am I on", "check my operating system", "my operating system", "what operating system am I using"
        ]
    },
    "what distro am I running": {
        "interpret": True,
        "meta": False,
        "function": get_linux_distro,
        "prompt": "Computer, what distro am I running? For my Linux distro, let me me know that this system is running: ",
        "alt": [ 
            "whats my linux distribution", "identify my linux distribution", "which linux distro am I using", "find my linux distro", "determine my linux distro", "linux distro details", "get my linux distribution info", "reveal my linux distro", "what linux distribution am I on", "check my linux distribution", "my linux distribution"
        ]
    },
    "get the news": {
        "interpret": True,
        "meta": False,
        "function": get_news,
        "prompt": "Computer, get the news. Get the latest news and provide me with a summary: ",
        "alt": [
            "get news data", "whats the news", "check news", "get news data", "hows the news",
            "whats the news like", "tell me the news", "news update", "current news",
            "news forecast", "news today", "news conditions", "give me the news",
            "local news", "show me the news"
        ]
    }

}
