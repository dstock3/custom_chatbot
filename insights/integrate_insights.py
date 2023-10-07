from model.insights import get_insights

def fetch_basic_insights(user):
    basic = get_insights(user["user_id"]).get('basic', {})
    return basic["data"]

def fetch_health_insights(user):
    health = get_insights(user["user_id"]).get('health', {})
    return health["data"]

def fetch_work_insights(user):
    work = get_insights(user["user_id"]).get('work', {})
    return work["data"]

def fetch_family_insights(user):
    family = get_insights(user["user_id"]).get('fam', {})
    return family["data"]

def fetch_personality_insights(user):
    personality = get_insights(user["user_id"]).get('big5', {})
    return personality["data"]

def fetch_entertainment_insights(user):
    entertainment = get_insights(user["user_id"]).get('ent', {})
    return entertainment["data"]

def respond_based_on_category(user, transcript=None):
    insights = fetch_basic_insights(user)

    if transcript:
        category = transcript[4]

        category_functions = {
            'Health & Fitness': fetch_health_insights,
            'Work & Productivity': fetch_work_insights,
            'Home & Family': fetch_family_insights,
            'Personal Development & Learning': fetch_personality_insights,
            'Entertainment & Leisure': fetch_entertainment_insights
        }

        if category in category_functions:
            specific_insights = category_functions[category](user)
            insights.extend(specific_insights)
    return insights





