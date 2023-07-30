import openai

def apiCall(prompt, maxTokens, temp):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[prompt],
        max_tokens=maxTokens,
        n=1,
        stop=["Assistant:", "User:"],
        temperature=temp,
    )
    return response["choices"][0]["message"]["content"]