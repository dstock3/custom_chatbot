import openai

def apiCall(prompt, maxTokens, temp, isChat=False):
    print("OpenAI API Call")
    for i in prompt:
        print("Prompt #" + str(prompt.index(i) + 1) +": " + str(i))

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt,
        max_tokens=maxTokens,
        n=1,
        stop=["Assistant:", "User:"],
        temperature=temp,
    )
    if isChat:
        return response
    else:
        return response["choices"][0]["message"]["content"]