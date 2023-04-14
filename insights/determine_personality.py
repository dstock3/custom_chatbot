def determine_personality_score(answers):
    #need to modify to use dict established in questions.py
    traits = {
        "Openness": ["openness1", "openness2"],
        "Conscientiousness": ["conscientiousness1", "conscientiousness2"],
        "Extraversion": ["extraversion1", "extraversion2"],
        "Agreeableness": ["agreeableness1", "agreeableness2"],
        "Neuroticism": ["neuroticism1", "neuroticism2"],
    }
    
    scores = {trait: 0 for trait in traits}
    
    for trait, questions in traits.items():
        for question in questions:
            scores[trait] += answers[question]
        scores[trait] /= len(questions)
    
    return scores

def interpret_personality_scores(scores):
    interpretations = {
        "Openness": {
            1: "You are very conventional and prefer sticking to familiar experiences.",
            3: "You have a balance between being open to new experiences and valuing tradition.",
            5: "You are very open to new experiences and have a strong appreciation for creativity and the arts.",
        },
        "Conscientiousness": {
            1: "You tend to be spontaneous and may struggle with organization and planning.",
            3: "You have a balance between being organized and spontaneous.",
            5: "You are highly organized, responsible, and reliable.",
        },
        "Extraversion": {
            1: "You are introverted and prefer solitude or small group settings.",
            3: "You have a balance between being introverted and extraverted.",
            5: "You are extraverted and enjoy being the center of attention in social situations.",
        },
        "Agreeableness": {
            1: "You tend to prioritize your own needs over those of others.",
            3: "You have a balance between being cooperative and assertive.",
            5: "You are very compassionate, cooperative, and have great concern for the well-being of others.",
        },
        "Neuroticism": {
            1: "You are emotionally stable and handle stress well.",
            3: "You have a balance between emotional stability and sensitivity to stress.",
            5: "You are emotionally sensitive and may experience frequent mood swings or stress.",
        },
    }

    response = "Here's the interpretation of your personality traits:\n"
    
    for trait, score in scores.items():
        rounded_score = round(score)
        interpretation = interpretations[trait][rounded_score]
        response += f"{trait}: {interpretation}\n"

    return response