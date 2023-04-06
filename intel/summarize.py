import openai

import openai

def summarize(messages, user):
    ai_name = user["system_name"]
    user_name = user["name"]
    
    try:
        summary = ''
        for exchange in messages:
            summary += user_name + ": " + exchange['user_message'] + " "
            summary += ai_name + ": " + exchange['assistant_message'] + " "

        summary_prompt = {
            "role": "assistant",
            "content": f"Summarize the following conversation: {summary}"
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[summary_prompt],
            max_tokens=250,
            n=1,
            stop=["Assistant:", "User:"],
            temperature=0.5,
        )

        if "choices" not in response or len(response["choices"]) == 0:
            raise Exception("Invalid response from OpenAI API")

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while summarizing the conversation."

    
