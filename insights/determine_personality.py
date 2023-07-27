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
    
    return insights
