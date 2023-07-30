from intel.openai_call import apiCall

def synthesize(summaries):
    prompt = "Synthesize the following summaries for your working memory: \n"
    for summary in summaries:
        prompt += summary + "\n"
    prompt += "Summary:"

    response = apiCall(prompt, 350, .7)

    return response