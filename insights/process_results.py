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