import openai

def summarize(messages):
    # This function takes in the transcript and returns a summary.
    summary = ''
    for exchange in messages:
        summary += exchange['user_message'] + " "
        summary += exchange['assistant_message'] + " "

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,
            n=1,
            stop=["Assistant:", "User:"],
            temperature=0.5,
        )

    summary_text = response.choices[0].text.strip()
    return summary_text
    
