import openai

def big5_results(data):
    traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    scores = {trait: 0 for trait in traits}

    for response in data:
        trait_type = response['type'][:-1]
        answer = int(response['response'][0])

        if trait_type in scores:
            scores[trait_type] += answer
    
    insights = {}
    for trait, score in scores.items():
        if score <= 2:
            insights[trait] = "Very low"
        elif score <= 4:
            insights[trait] = "Low"
        elif score <= 6:
            insights[trait] = "Neutral"
        elif score <= 8:
            insights[trait] = "High"
        else:
            insights[trait] = "Very high"

    insight_text = ', '.join(f'{trait}: {description}' for trait, description in insights.items())
    prompt = (f"I've analyzed the individual's responses on the Big Five personality traits. "
              f"Here are the insights: {insight_text}. "
              f"Please provide key insights to optimize the individual's life, "
              f"and formulate the insights as though you are speaking directly to them.")

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
        max_tokens=250,
        n=1,
        stop=["Assistant:", "User:"],
        temperature=.7,
    )

    summary = response['choices'][0]['message']['content'] if response['choices'] else ""

    return summary

