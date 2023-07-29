import openai

def big5_results(data):
    traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    scores = {trait: 0 for trait in traits}

    for response in data:
        trait_type = response['type'][:-1]
        answer = int(response['response'][0])

        if trait_type in scores:
            scores[trait_type] += answer
    
    results = {}
    for trait, score in scores.items():
        if score <= 2:
            results[trait] = "Very low"
        elif score <= 4:
            results[trait] = "Low"
        elif score <= 6:
            results[trait] = "Neutral"
        elif score <= 8:
            results[trait] = "High"
        else:
            results[trait] = "Very high"
    
    results = {trait.capitalize(): description for trait, description in results.items()}

    results_text = ', '.join(f'{trait}: {description}' for trait, description in results.items())
    prompt = (f"The following are an individual's responses on the Big Five personality traits. "
              f"Here are the results: {results_text}. "
              f"Please provide key insights to optimize this person's life, "
              f"and formulate the insights as though you are speaking directly to them. "
              f"Make sure to be fairly concise. Do not formulate lists.")

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
        max_tokens=150,
        n=1,
        stop=["Assistant:", "User:"],
        temperature=.8,
    )

    summary = response['choices'][0]['message']['content'] if response['choices'] else ""

    return results, summary

