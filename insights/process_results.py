def process_results(responses):
    results = {
        "basics": {},
        "personality": {},
        "health": {},
        "family": {},
        "work": {}
    }

    for category, questions in questions.items():
        for question in questions:
            question_id = question["id"]
            response = responses.get(question_id)
            if response is not None:
                results[category][question_id] = response

    return results