import os
import subprocess

def process_system_command(user_input, system_commands):
    if user_input in system_commands:
        cmd = system_commands[user_input]
        subprocess.run(cmd, shell=True)
    else:
        os.system(user_input)

def process_custom_command(user_input, custom_commands):
    if user_input in custom_commands:
        if custom_commands[user_input]["interpret"]:
            return {"interpret": "true", "function": custom_commands[user_input]["function"], "prompt": custom_commands[user_input]["prompt"]}
        else:
            return {"interpret": "false", "function": custom_commands[user_input]["function"]}
            
