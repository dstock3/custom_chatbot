from gtts import gTTS
import os
import openai, config
from intel.personalities import personalities
from system.systemCommands import system_commands
from system.customCommands import custom_commands
from system.processCommand import process_system_command, process_custom_command
from system.determineOS import determine_os
import string

openai.api_key = config.OPENAI_API_KEY
chat_model = "gpt-3.5-turbo"
transcription_model = "whisper-1"
personality = personalities["technical"]
os_name = determine_os()
ai_name = "computer"

def parse_transcript(text, operating_system):
    # This function takes in the transcript and parses it to see if the user gave a command. If the user gave a command, it returns the command. Otherwise, it returns None.

    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    command = None
    commandType = None

    # system commands can be parsed normally
    for cmd in system_commands[operating_system]:
        if cmd in text:
            if ai_name + " " + cmd in text:
                command = cmd
                commandType = "system"
    # commands that need to be parsed differently
    for cmd in custom_commands:
        if cmd in text:
            if ai_name + " " + cmd in text:
                command = cmd
                commandType = "custom"
            command = cmd

    return {"command": command, "command-type": commandType}
    
def process_input(audio_file, messages):
    # This function takes in the audio file and the messages. To boot, it uses the OpenAI whisper model to transcribe the audio file. 
    with open(audio_file, "rb") as f:
        transcript = openai.Audio.transcribe(transcription_model, f)
        commandInfo = parse_transcript(transcript["text"], os_name)
        command = commandInfo["command"]
        commandType = commandInfo["command-type"]
        if command is not None:
            # If the user gives a command, we don't want to add it to the chat transcript.Instead, we want to process the command and then return a message to the user.

            if commandType == "custom":
                process_custom_command(command, custom_commands)
            elif commandType == "system":
                process_system_command(command, system_commands[os_name])
        else:
            # If the user doesn't give a command, we want to add the transcript to the chat transcript and then generate a response from the chat model.
            user_message = {"role": "user", "content": transcript["text"]}
            messages.append(user_message)
            
            return messages

def generate_response(messages):
    # This function actually generates the response from the chat model. It takes in the messages and returns the system message and the updated messages.
    response = openai.ChatCompletion.create(model=chat_model, messages=messages, temperature=personality["temperature"])
    system_message = response["choices"][0]["message"]
    messages.append(system_message)
    return system_message, messages

def convert_to_audio(system_message):
    # This function takes in the system message and converts it to audio. It uses the gTTS library to convert the text to speech.
    tts = gTTS(system_message['content'], tld='com.au', lang='en', slow=False)
    tts.save('output.mp3')
    os.system('vlc --play-and-exit output.mp3 vlc://quit >/dev/null 2>&1 --qt-start-minimized')

def create_chat_transcript(messages):
    # This function takes in the messages and returns a chat transcript. It is used to display the chat transcript to the user.
    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"
    return chat_transcript

def main(audio_file):
    # The main function is the function that is called when the user interacts with the interface. It takes in the audio file and returns the chat transcript.
    try:
        messages = process_input(audio_file, personality["messages"])
        
        if messages:
            # If the user didn't give a command, we want to generate a response.
            system_message, messages = generate_response(messages)
            convert_to_audio(system_message)
            chat_transcript = create_chat_transcript(messages)
            return chat_transcript
        
    except Exception as e:
        return "An error occurred: {}".format(str(e))