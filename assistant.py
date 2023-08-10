from gtts import gTTS
import subprocess
import openai, config
from intel.personalities import personalities
from system.systemCommands import system_commands
from system.customCommands import custom_commands
from system.processCommand import process_system_command, process_custom_command
from system.determineOS import determine_os
from intel.emoji import extract_emojis
import re

#types
from type.basicTypes import checkInstance, IsAudio, Input, ChatTranscript
from type.systemMessage import SystemMessage
from typing import Dict, Any, List

openai.api_key = config.OPENAI_API_KEY
transcription_model = "whisper-1"
os_name = determine_os()

def parse_transcript(text: str, operating_system: str, ai_name: str):
    checkInstance(text, str)
    checkInstance(operating_system, str)

    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    ai_name = ai_name.lower()

    all_commands = [
        ("system", system_commands[operating_system]),
        ("custom", custom_commands.keys())
    ]

    for command_type, commands in all_commands:
        for cmd in commands:
            if ai_name + " " + cmd in text:
                return {"command": cmd, "command-type": command_type}
            elif command_type == "custom":
                for alt_cmd in custom_commands[cmd]['alt']:
                    if ai_name + " " + alt_cmd in text:
                        return {"command": cmd, "command-type": command_type}

    return {"command": None, "command-type": None}

def process_command(command, commandType, messages, file):
    if command is not None:
        if commandType == "custom":
            process_custom_command(command, custom_commands, messages, file)
        elif commandType == "system":
            process_system_command(command, system_commands[os_name])
        return messages, True
    else:
        user_message = {"role": "user", "content": file}
        messages.append(user_message)

        return messages, False

def process_input(isAudio: IsAudio, file, messages, ai_name: str):
    if isAudio:
        with open(file, "rb") as f:
            transcript = openai.Audio.transcribe(transcription_model, f)
            text = transcript["text"]
    else:
        text = file

    commandInfo = parse_transcript(text, os_name, ai_name)
    command = commandInfo["command"]
    commandType = commandInfo["command-type"]
    messages, isCommand = process_command(command, commandType, messages, text)

    return messages, isCommand, command

def derive_model_response(model, messages, temperature, ai_name):
    if (model == "gpt-3.5-turbo") or (model == "gpt-4"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=250,
            n=1,
            stop=["Assistant:", "User:"],
            temperature=temperature,
        )
    else:
        conversation_history = "".join(f"{message['role'].capitalize()}: {message['content']}\n" for message in messages)
        prompt = f"{conversation_history}{ai_name}:"
        completion_response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=250,
            n=1,
            stop=["\n"],
            temperature=temperature,
        )
        response = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": completion_response.choices[0].text.strip(),
                    }
                }
            ]
        }
    return response

def generate_response(messages, temperature, model, ai_name):
    emoji_check = None
    display = None

    response = derive_model_response(model, messages, temperature, ai_name)

    emoji_check, cleaned_text = extract_emojis(response["choices"][0]["message"]["content"])

    if emoji_check:
        display = emoji_check[0]
        system_message = {"content": cleaned_text, "role": "assistant"}
    else:
        system_message = response["choices"][0]["message"]

    messages.append(system_message)
    return system_message, messages, display

def convert_to_audio(system_message: SystemMessage) -> None:
    # This function takes in the system message and converts it to audio. It uses the gTTS library to convert the text to speech.
    tts = gTTS(system_message['content'], tld='com.au', lang='en', slow=False)
    tts.save('output.mp3')

    # Use subprocess to launch VLC player in a separate process
    subprocess.Popen(['vlc', '--play-and-exit', 'output.mp3', 'vlc://quit', '--qt-start-minimized'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def create_chat_transcript(messages: List[Dict[str, Any]], isCommand: bool, command: str or None, ai_name: str) -> List[Dict[str, str]]:
    chat_transcript = []
    user_message = ''
    assistant_message = ''
    prev_command_set = None

    for index, message in enumerate(messages):
        if message['role'] == 'user':
            prev_command_set = parse_transcript(message['content'], os_name, ai_name)
            
            if prev_command_set["command"] is not None:
                user_message += prev_command_set['command']
            else:
                user_message += message['content']
        elif message['role'] == 'assistant':
            assistant_message += message['content']

            if isCommand and index == len(messages) - 1:
                chat_transcript.append({'user_message': command, 'assistant_message': assistant_message})
            else:
                chat_transcript.append({'user_message': user_message, 'assistant_message': assistant_message})

            user_message = ''
            assistant_message = ''

    return chat_transcript

def main(
        user: object,
        isAudio: IsAudio, 
        input: Input = None,
        existing_messages = None
    ) -> ChatTranscript:

    if user is not None:
        name = user['name']
        voice_command = user['voice_command']
        voice_response = user['voice_response']
        model = user['model']
        personality = user['personality']
        ai_name = user['system_name']

    chat_transcript: ChatTranscript = {}
    display = None

    personality_data = personalities.get(personality)

    if input is not None:
        try:
            if existing_messages:
                messages = personality_data["messages"] + existing_messages
                messages, isCommand, command = process_input(isAudio, input, messages, ai_name)
            else:
                messages, isCommand, command = process_input(isAudio, input, personality_data["messages"], ai_name)
            
            if messages:
                name_message = {
                    "role": "system",
                    "content": f"Hello, I am {name}. You are my AI assistant named {ai_name}. "
                        f"Please remember to address yourself as {ai_name} and address me as {name}. "
                        f"Additionally, if you provide any code snippets, mark the beginning with '%%%CODE_START%%%' "
                        f"and the end with '%%%CODE_END%%%' After that, let me know the specific language being used within a separate block. Make sure the language is accurate. Mark the beginning with '%%%LANGUAGE_START%%%' and the end with '%%%LANGUAGE_END%%%'."
                }
                messages.insert(0, name_message)
                system_message, messages, display = generate_response(messages, personality_data["temperature"], model, ai_name)
                if voice_response:
                    convert_to_audio(system_message)
                chat_transcript = create_chat_transcript(messages, isCommand, command, ai_name)

        except Exception as e:
            chat_transcript['assistant_message'] = "An error occurred: {}".format(str(e))

    return chat_transcript, display