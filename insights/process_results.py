import openai
from insights.determine_personality import big5_results

def get_summary(insights):
    summary = ""
    if insights:
        summary = ' '.join(f"{insight['question']} {insight['response']}" for insight in insights)

    prompt = f"Analyze the following survey data and provide key insights to optimize the individual's life. Formulate the insights as though you are speaking directly to them. Make sure to be fairly concise. Here's the survey data: {summary}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a data analyst with a specialty in psychology and sociology."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=200,
        n=1,
        stop=["Assistant:", "User:"],
        temperature=.7,
    )

    summary = response['choices'][0]['message']['content'] if response['choices'] else ""
    return summary

def get_category(key):
    if key.startswith("basic"):
        return "basic"
    elif key.startswith(("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism")):
        return "big5"
    elif key.startswith("health"):
        return "health"
    elif key.startswith("family"):
        return "fam"
    elif key.startswith("work"):
        return "work"
    else:
        return None

def process_results(responses):
    insights = {
        'basic': {"summary": "", "data": []},
        'health': {"summary": "", "data": []},
        'fam': {"summary": "", "data": []},
        'work': {"summary": "", "data": []},
        'big5': {"summary": "", "results": "", "data": []},
    }

    for key, question_response in responses.items():
        category = get_category(key)
        if category:
            for question, response in question_response.items():
                insights[category]["data"].append({
                    "question": question,
                    "response": response,
                    "type": key
                })

    for category in insights:
        if category == "big5":
            results, summary = big5_results(insights[category]["data"])  
            insights[category]["summary"] = summary
            insights[category]["results"] = results
        else:
            if insights[category]["data"]:
                summary = get_summary(insights[category]["data"])
                insights[category]["summary"] = summary

    return insights

