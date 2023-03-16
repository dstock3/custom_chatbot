from gtts import gTTS
import subprocess
import openai, config
from intel.personalities import personalities
from system.systemCommands import system_commands
from system.customCommands import custom_commands
from system.processCommand import process_system_command, process_custom_command
from system.determineOS import determine_os
import re

#types
from type.basicTypes import checkInstance, IsAudio, Input, ChatTranscript
from type.systemMessage import SystemMessage
from typing import Dict, Any, List

openai.api_key = config.OPENAI_API_KEY
chat_model = "gpt-3.5-turbo"
transcription_model = "whisper-1"
personality = personalities["sardonic"]
os_name = determine_os()
ai_name = "computer"
voice_response = True

def parse_transcript(text: str, operating_system: str):
    checkInstance(text, str)
    checkInstance(operating_system, str)

    # This function takes in the transcript and parses it to see if the user gave a command. If the user gave a command, it returns the command. Otherwise, it returns None.

    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    command = None
    commandType = None
    
    for cmd in system_commands[operating_system]:
        if cmd in text:
            if ai_name + " " + cmd in text:
                command = cmd
                commandType = "system"
                break
    
    for cmd in custom_commands:
        if cmd in text:
            if ai_name + " " + cmd in text:
                command = cmd
                commandType = "custom"
                break
            command = cmd

    return {"command": command, "command-type": commandType}

def process_command(command, commandType, messages, file):
    if command is not None:
        if commandType == "custom":
            process_custom_command(command, custom_commands, messages)
        elif commandType == "system":
            process_system_command(command, system_commands[os_name])
    else:
        user_message = {"role": "user", "content": file}
        messages.append(user_message)
    
    return messages
    
def process_input(isAudio: IsAudio, file, messages):
    # This function takes in the audio file and the messages. it uses the OpenAI whisper model to transcribe the audio file.

    if isAudio:
        with open(file, "rb") as f:
            transcript = openai.Audio.transcribe(transcription_model, f)
            commandInfo = parse_transcript(transcript["text"], os_name)
            command = commandInfo["command"]
            commandType = commandInfo["command-type"]

            messages = process_command(command, commandType, messages, transcript["text"])

            return messages
    else:
        commandInfo = parse_transcript(file, os_name)
        command = commandInfo["command"]
        commandType = commandInfo["command-type"]

        messages = process_command(command, commandType, messages, file)

        return messages

def generate_response(messages):
    # This function generates the response from the chat model. It takes in the messages and returns the system message and the updated messages.
    response = openai.ChatCompletion.create(model=chat_model, messages=messages, temperature=personality["temperature"])
    system_message = response["choices"][0]["message"]
    messages.append(system_message)
    return system_message, messages

def convert_to_audio(system_message: SystemMessage) -> None:
    # This function takes in the system message and converts it to audio. It uses the gTTS library to convert the text to speech.
    tts = gTTS(system_message['content'], tld='com.au', lang='en', slow=False)
    tts.save('output.mp3')

    # Use subprocess to launch VLC player in a separate process
    subprocess.Popen(['vlc', '--play-and-exit', 'output.mp3', 'vlc://quit', '--qt-start-minimized'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def create_chat_transcript(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    # This function takes in the messages and returns an array of chat exchanges, with each exchange containing a user message and assistant message.
    checkInstance(messages, list)

    chat_transcript = []
    user_message = ''
    assistant_message = ''
    for message in messages:
        if message['role'] == 'user':
            user_message += message['content']
        elif message['role'] == 'assistant':
            assistant_message += message['content']
            chat_transcript.append({'user_message': user_message, 'assistant_message': assistant_message})
            user_message = ''
            assistant_message = ''

    # Add any remaining messages
    if user_message != '' or assistant_message != '':
        chat_transcript.append({'user_message': user_message, 'assistant_message': assistant_message})

    return chat_transcript

def main(isAudio: IsAudio, input: Input = None) -> ChatTranscript:
    # The main function is the function that is called when the user interacts with the interface. It takes in the audio file/text input and returns the chat transcript.
    checkInstance(isAudio, bool)
    chat_transcript: ChatTranscript = {}
    
    if input is not None:
        try:
            messages = process_input(isAudio, input, personality["messages"])

            if messages:
                system_message, messages = generate_response(messages)
                if voice_response:
                    convert_to_audio(system_message)
                chat_transcript = create_chat_transcript(messages)

        except Exception as e:
            chat_transcript['assistant_message'] = "An error occurred: {}".format(str(e))
            
    return chat_transcript