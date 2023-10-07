from intel.openai_call import apiCall
from model.intel import insert_analysis

def analysis(insights, user, transcript):
    # we perform an analysis every 5 messages
    if (len(transcript[2]) % 5 != 0):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that performs analysis based on data provided to you."},
            {"role": "user", "content": f"Perform an analysis of the user in following conversation. What insights can be observed from the user's language and behavior? {transcript[2]}"}
        ]
        analysis = apiCall(messages, 300, 0.8)
        insert_analysis(user["user_id"], transcript[0], analysis)
    elif (len(transcript[2]) % 8 != 0):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that performs analysis based on data provided to you."},
            {"role": "user", "content": f"Perform an analysis of the user in following conversation and compare it to what you already know about this user. Here's what you already know: {insights} Now, what insights can be observed from the user's language and behavior? {transcript[2]}"}
        ]
        analysis = apiCall(messages, 500, 0.9)
        insert_analysis(user["user_id"], transcript[0], analysis)
    

