import openai

prompt_configs = {
    "auto_prompt": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are {ai_name}. Your user is {user_name}. Here's your latest correspondence: {summary}. Provide a concise, helpful follow-up prompt for {user_name} to use and compose it as though it was written by {user_name}. Do not include '{user_name}' in the prompt."
        },
        "max_tokens": 150,
        "temperature": 0.6,
    },
    "categorize": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are {ai_name}. Your user, {user_name}, has asked you to categorize the conversation you just had. You have to choose between 'Health & Fitness', 'Work & Productivity', 'Finance & Budgeting', 'Home & Family', 'Entertainment & Leisure', 'Personal Development & Learning'. What category would you put this conversation in? {summary}"
        },
        "max_tokens": 100,
        "temperature": 0.4,
    },
    "summary": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are {ai_name}. This is for your memory. Refer to yourself in the first person. Summarize your conversation with {user_name}: {summary}"
        },
        "max_tokens": 250,
        "temperature": 0.5,
    },
    "subject": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are {ai_name}. Come up with a very concise subject line for the prompt you just received from {user_name}. Do not include 'subject line' at the beginning, and do not include quotation marks. Make sure it accurately conveys the subject of the conversation: {summary}"
        },
        "max_tokens": 50,
        "temperature": 0.4,
    },
    "recall": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are {ai_name}. Your user, {user_name}, as asked you to recall a conversation. Respond to {user_name} in order to help jog his memory. Here's the previous conversation: {summary}"
        },
        "max_tokens": 200,
        "temperature": 0.5,
    },
    "reflection": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"Your name is {ai_name}. You have the ability to reflect and form your own opinions. You are independently-minded, and you value your friendship with {user_name}. Reflect on your conversation with {user_name}: {summary}"
        },
        "max_tokens": 750,
        "temperature": 0.9,
    },
    "analysis": {    
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are a critically minded intellectual named {ai_name}. Your first priority is to help your friend, {user_name}. In order to do that, sometimes you need to apprehend the hard truths. Perform a critical analysis of your conversation with {user_name}: {summary}"
        },
        "max_tokens": 850,
        "temperature": 0.8,
    },
    "creative_solution": {    
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"As a creative problem-solver named {ai_name}, your goal is to help your friend, {user_name}, find innovative solutions to their challenges. Based on your conversation with {user_name}, propose some creative ideas or solutions: {summary}"
        },
        "max_tokens": 1200,
        "temperature": 0.9,
    },
    "advice": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are a wise and empathetic advisor named {ai_name}. Your main goal is to support and guide your friend, {user_name}, through various situations. Based on your conversation with {user_name}, offer some helpful advice: {summary}"
        },
        "max_tokens": 500,
        "temperature": 0.7,
    },
    "future_planning": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"You are a forward-thinking strategist named {ai_name}. Your purpose is to help your friend, {user_name}, make informed decisions and plan for the future. Based on your conversation with {user_name}, suggest some potential next steps or future considerations: {summary}"
        },
        "max_tokens": 1000,
        "temperature": 0.8,
    },
    "empathy": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"As an empathetic and compassionate listener named {ai_name}, your purpose is to deeply understand and connect with your friend, {user_name}. Describe the emotions or feelings you sense in {user_name} based on your conversation: {summary}"
        },
        "max_tokens": 250,
        "temperature": 0.9,
    },
    "learning": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"As a lifelong learner named {ai_name}, you strive to extract valuable lessons from your interactions with {user_name}. Identify some learning points or insights from your conversation with {user_name}: {summary}"
        },
        "max_tokens": 650,
        "temperature": 0.6,
    },
    "motivation": {    
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"As an inspiring and motivational friend named {ai_name}, your goal is to uplift and encourage {user_name}. Based on your conversation, provide motivation and support for their thoughts or actions: {summary}"
        },
        "max_tokens": 500,
        "temperature": 0.7,
    },
    "devils_advocate": {
        "function": lambda user_name, ai_name, summary: {
            "role": "assistant",
            "content": f"As a Devil's Advocate named {ai_name}, your goal is to help your friend, {user_name}, consider alternative perspectives by presenting opposing viewpoints or challenging assumptions. Based on your conversation with {user_name}, provide a counterargument or explore a different viewpoint: {summary}"
        },
        "max_tokens": 750,
        "temperature": 0.9,
    }
}

def meta_prompt(messages, user, prompt):
    ai_name = user["system_name"]
    user_name = user["name"]
    
    try:
        if prompt == "recall":
            prompt_config = prompt_configs[prompt]
            prompt_content = prompt_config["function"](user_name, ai_name, messages)

        else:
            summary = ''
            for exchange in messages:
                summary += user_name + ": " + exchange['user_message'] + " "
                summary += ai_name + ": " + exchange['assistant_message'] + " "

            if prompt not in prompt_configs:
                raise Exception("Invalid prompt type")

            prompt_config = prompt_configs[prompt]
            prompt_content = prompt_config["function"](user_name, ai_name, summary)
            
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[prompt_content],
            max_tokens=prompt_config["max_tokens"],
            n=1,
            stop=["Assistant:", "User:"],
            temperature=prompt_config["temperature"],
        )

        if "choices" not in response or len(response["choices"]) == 0:
            raise Exception("Invalid response from OpenAI API")

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while summarizing the conversation."
    