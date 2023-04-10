import os
import subprocess

def process_system_command(user_input, system_commands):
    if user_input in system_commands:
        cmd = system_commands[user_input]
        subprocess.run(cmd, shell=True)
    else:
        os.system(user_input)

def process_custom_command(user_input, custom_commands, messages, file):
    print(f"Processing custom command: {user_input}")
    if user_input in custom_commands:
        if custom_commands[user_input]["interpret"]:
            if custom_commands[user_input]["meta"]:
                result = custom_commands[user_input]["function"](file)
                
                user_input = {"role": "user", "content": file}
                assistant_message = {"role": "assistant", "content": result}
                messages.append(user_input)
                messages.append(assistant_message)
            else:
                result = custom_commands[user_input]["function"]()
                user_message = {"role": "user", "content": custom_commands[user_input]["prompt"] + str(result)}
                messages.append(user_message)
        else:
            #if the interpret flag is false, the function will return the message to be displayed instead of prompting the API
            result = custom_commands[user_input]["function"]()
            print(result)
            assistant_message = {"role": "assistant", "content": custom_commands[user_input]["prompt"] + str(result)}
            messages.append(assistant_message)
    return messages


            
