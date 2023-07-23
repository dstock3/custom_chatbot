def process_results(responses, questions):
    insights = []

    for category, category_questions in questions.items():
        for question in category_questions:
            question_id = question["id"]
            response = responses.get(category, {}).get(question_id)
            if response is not None:
                insights.append({
                    "question": question["text"],
                    "response": response
                })

    return insights
