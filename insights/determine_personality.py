def big5_results(data):
    traits = {
        'openness': ['I have a vivid imagination.', 'I am interested in abstract ideas.'],
        'conscientiousness': ['I am always prepared.', 'I am a reliable worker.'],
        'extraversion': ['I am the life of the party.', 'I feel comfortable around people.'],
        'agreeableness': ['I am helpful and unselfish with others.', 'I have a good relationship with my neighbors.'],
        'neuroticism': ['I often feel sad.', 'I get stressed out easily.'],
    }
    
    scores = {trait: 0 for trait in traits}

    for response in data:
        question = response['question']
        answer = int(response['response'][0])
        
        for trait, questions in traits.items():
            if question in questions:
                scores[trait] += answer
    
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
