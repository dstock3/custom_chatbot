import openai

def get_sentiment(text):
    # This function takes in the transcript and returns a sentiment analysis.
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Perform a sentiment analysis of the following text: '{text}'",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    sentiment = response.choices[0].text.strip().lower()

    if sentiment == "positive":
        return 1
    elif sentiment == "negative":
        return -1
    else:
        return 0