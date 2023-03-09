Intel

personalities.py

The repository features a Python script named "personalities.py", which implements a dictionary data structure to define and manage a diverse array of personality types for a chatbot assistant. Each personality type serves as a key in the dictionary, and the corresponding value is another dictionary that contains two key-value pairs: "messages" and "temperature".

The "messages" key in the dictionary contains a list of dictionaries that encapsulate the chatbot's responses to user inputs, with each message explicitly indicating its role as either "system" or "user". Meanwhile, the "temperature" key stores a floating-point value that determines the chatbot's level of creativity and spontaneity.

The messages predefined for each personality type offer a succinct exposition of the character's traits and attributes, as well as their intended conversational style. The temperature values range from 0 to 1, with lower values signifying predictable and cautious responses, while higher values signify more inventive and capricious responses.

Developers can use the "personalities.py" script as a building block for creating and customizing chatbots that exhibit a wide range of conversational styles, catering to diverse user needs and preferences.


System 

systemCommands.py

 This dictionary is organized into three hierarchical levels of keys and values, with the first level consisting of three distinct strings: "ubuntu", "windows", and "mac", each representing a unique operating system.

Each of these first-level keys maps to a nested dictionary as its corresponding value. These nested dictionaries contain a collection of key-value pairs, where each key is a string representing a specific system command (e.g., "restart" or "shutdown"), and the corresponding value is a string representing the executable command itself.

To illustrate, for the Ubuntu operating system, the dictionary comprises system commands like "restart", which maps to the command "sudo shutdown -r now", and "search", which maps to the command "sudo apt search". Similarly, for the Windows operating system, the dictionary includes commands such as "restart", which maps to the command "shutdown /r /t 0", and "search", which maps to the command "winget search". Finally, for the macOS operating system, the dictionary encompasses commands such as "restart", which maps to the command "sudo shutdown -r now", and "search", which maps to the command "brew search".

The "system_commands" dictionary serves as a convenient means to retrieve frequently used system commands for each operating system. By utilizing the appropriate key for the desired operating system, and then accessing the specific command key, the corresponding command string can be retrieved and executed with ease.