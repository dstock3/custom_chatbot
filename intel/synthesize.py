import openai

def synthesize(summaries):
    #this function takes a list of summaries and calls the openai api to generate a synthesis of the summaries
    prompt = "Synthesize the following summaries for your working memory: \n"
    for summary in summaries:
        prompt += summary + "\n"
    prompt += "Summary:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[prompt],
        max_tokens=350,
        n=1,
        stop=["Assistant:", "User:"],
        temperature=.7,
    )
    return response["choices"][0]["message"]["content"]