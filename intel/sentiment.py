from intel.openai_call import apiCall
    
def get_sentiment(input):
    # This function takes in the transcript and returns a sentiment analysis.
    messages = [
        {"role": "system", "content": "You are a helpful assistant that performs sentiment analysis."},
        {"role": "user", "content": f"Perform a sentiment analysis of the following text. Return a response of either 'positive,' 'negative,' or 'neutral': {input}"}
    ]

    response = apiCall(messages, 50, .7)
    
    content = response.choices[0].message['content'].strip()
    sentiment = None

    if "positive" in content.lower():
        sentiment = "positive"
    elif "negative" in content.lower():
        sentiment = "negative"
    elif "neutral" in content.lower():
        sentiment = "neutral"

    if sentiment == "positive":
        return 1
    elif sentiment == "negative":
        return -1
    else:
        return 0