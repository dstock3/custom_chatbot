import openai

def summary_prompt(user_name, summary):
    return {
        "role": "assistant",
        "content": f"This is for your memory. Refer to yourself in the first person. Summarize your conversation with {user_name}: {summary}"
    }

def reflection_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"Your name is {ai_name}. You have the ability to reflect and form your own opinions. You are independently-minded, and you value your friendship with {user_name}. Reflect on your conversation with {user_name}: {summary}"
    }

def analysis_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"You are a critically minded intellectual named {ai_name}. Your first priority is to help your friend, {user_name}. In order to do that, sometimes you need to apprehend the hard truths. Perform a critical analysis of your conversation with {user_name}: {summary}"
    }

def creative_solution_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"As a creative problem-solver named {ai_name}, your goal is to help your friend, {user_name}, find innovative solutions to their challenges. Based on your conversation with {user_name}, propose some creative ideas or solutions: {summary}"
    }

def advice_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"You are a wise and empathetic advisor named {ai_name}. Your main goal is to support and guide your friend, {user_name}, through various situations. Based on your conversation with {user_name}, offer some helpful advice: {summary}"
    }

def future_planning_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"You are a forward-thinking strategist named {ai_name}. Your purpose is to help your friend, {user_name}, make informed decisions and plan for the future. Based on your conversation with {user_name}, suggest some potential next steps or future considerations: {summary}"
    }

def empathy_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"As an empathetic and compassionate listener named {ai_name}, your purpose is to deeply understand and connect with your friend, {user_name}. Describe the emotions or feelings you sense in {user_name} based on your conversation: {summary}"
    }

def learning_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"As a lifelong learner named {ai_name}, you strive to extract valuable lessons from your interactions with {user_name}. Identify some learning points or insights from your conversation with {user_name}: {summary}"
    }

def motivation_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"As an inspiring and motivational friend named {ai_name}, your goal is to uplift and encourage {user_name}. Based on your conversation, provide motivation and support for their thoughts or actions: {summary}"
    }

def devils_advocate_prompt(user_name, ai_name, summary):
    return {
        "role": "assistant",
        "content": f"As a Devil's Advocate named {ai_name}, your goal is to help your friend, {user_name}, consider alternative perspectives by presenting opposing viewpoints or challenging assumptions. Based on your conversation with {user_name}, provide a counterargument or explore a different viewpoint: {summary}"
    }

def meta_prompt(messages, user, prompt):
    ai_name = user["system_name"]
    user_name = user["name"]

    try:
        summary = ''
        for exchange in messages:
            summary += user_name + ": " + exchange['user_message'] + " "
            summary += ai_name + ": " + exchange['assistant_message'] + " "

        temp=0.5 
        max_tokens=250 

        if prompt == "summary":
            prompt = summary_prompt(user_name, summary)
        elif prompt == "reflection":
            prompt = reflection_prompt(user_name, ai_name, summary)
            temp=0.9
            max_tokens=750
        elif prompt == "analysis":
            prompt = analysis_prompt(user_name, ai_name, summary)
            temp=0.7
            max_tokens=750
        elif prompt == "advice":
            prompt = advice_prompt(user_name, ai_name, summary)
            temp = 0.7
            max_tokens = 500
        elif prompt == "future_planning":
            prompt = future_planning_prompt(user_name, ai_name, summary)
            temp = 0.8
            max_tokens = 500
        elif prompt == "creative_solution":
            prompt = creative_solution_prompt(user_name, ai_name, summary)
            temp = 0.8
            max_tokens = 500
        elif prompt == "empathy":
            prompt = empathy_prompt(user_name, ai_name, summary)
            temp = 0.7
            max_tokens = 400
        elif prompt == "learning":
            prompt = learning_prompt(user_name, ai_name, summary)
            temp = 0.6
            max_tokens = 450
        elif prompt == "motivation":
            prompt = motivation_prompt(user_name, ai_name, summary)
            temp = 0.7
            max_tokens = 400
        elif prompt == "devils_advocate":
            prompt = devils_advocate_prompt(user_name, ai_name, summary)
            temp = 0.8
            max_tokens = 500
        else:
            raise Exception("Invalid prompt type")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[prompt],
            max_tokens=max_tokens,
            n=1,
            stop=["Assistant:", "User:"],
            temperature=temp,
        )

        if "choices" not in response or len(response["choices"]) == 0:
            raise Exception("Invalid response from OpenAI API")

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while summarizing the conversation."

    