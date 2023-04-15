from intel.meta_prompt import meta_prompt
from model.user import get_user
import re

def determine_category(chat_transcript):
    user = get_user()
    
    system_response = meta_prompt(chat_transcript, user, 'categorize')
    
    categories = ['Health & Fitness', 'Work & Productivity', 'Finance & Budgeting', 'Home & Family', 'Entertainment & Leisure', 'Personal Development & Learning']
    
    for category in categories:
        if category in system_response:
            return category
    return None


