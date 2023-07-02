def process_results(responses):
    insights = []

    for category, questions in questions.items():
        for question in questions:
            question_id = question["id"]
            response = responses.get(category).get(question_id)
            if response is not None:
                insights.append({
                    "question": question["text"],
                    "response": response
                })

    return insights

def calculate_big_five_scores(responses):
    traits = {
        'Openness': ['openness1', 'openness2'],
        'Conscientiousness': ['conscientiousness1', 'conscientiousness2'],
        'Extraversion': ['extraversion1', 'extraversion2'],
        'Agreeableness': ['agreeableness1', 'agreeableness2'],
        'Neuroticism': ['neuroticism1', 'neuroticism2']
    }
    
    scores = {}
    
    for trait, questions in traits.items():
        score = 0
        for question_id in questions:
            # Get the numeric value from the response (e.g. '5 - Strongly agree' -> 5)
            score += int(responses[question_id].split(' ')[0])
        scores[trait] = score
    
    return scores
