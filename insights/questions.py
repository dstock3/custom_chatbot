questions = {
    "basics": [
        {
            "id": "basic1",
            "text": "What is your age?",
            "type": "text"
        },
        {
            "id": "basic2",
            "text": "What is your gender?",
            "type": "select",
            "options": ["Male", "Female", "Non-binary", "Prefer not to say", "Other"]
        },
        {
            "id": "basic3",
            "text": "What is your highest level of education?",
            "type": "select",
            "options": ["No formal education", "Primary education", "Secondary education", "Vocational/technical training", "Bachelor's degree", "Master's degree", "Doctorate or higher", "Other"]
        },
        {
            "id": "basic4",
            "text": "What is your current employment status?",
            "type": "select",
            "options": ["Employed full-time", "Employed part-time", "Self-employed", "Unemployed", "Student", "Retired", "Homemaker", "Other"]
        },
        {
            "id": "basic5",
            "text": "What is your annual income range?",
            "type": "select",
            "options": ["Under $25,000", "$25,000 - $49,999", "$50,000 - $74,999", "$75,000 - $99,999", "$100,000 - $149,999", "$150,000 - $199,999", "$200,000 and above", "Prefer not to say"]
        },
        {
            "id": "basic6",
            "text": "What is your country of residence?",
            "type": "select",
            "options": ["Country 1", "Country 2", "Country 3", "..."]  # Replace with a list of actual countries
        },
        {
            "id": "basic7",
            "text": "What is your ethnicity?",
            "type": "select",
            "options": ["Ethnicity 1", "Ethnicity 2", "Ethnicity 3", "..."]  # Replace with a list of actual ethnicities
        },
        {
            "id": "basic8",
            "text": "What is your relationship status?",
            "type": "select",
            "options": ["Single", "Married", "In a relationship", "Divorced", "Widowed", "Separated", "It's complicated", "Prefer not to say"]
        },
    ],
    "personality": [
        {
            "id": "openness1",
            "text": "I have a vivid imagination.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "openness2",
            "text": "I am interested in abstract ideas.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "conscientiousness1",
            "text": "I am always prepared.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "conscientiousness2",
            "text": "I am a reliable worker.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "extraversion1",
            "text": "I am the life of the party.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "extraversion2",
            "text": "I feel comfortable around people.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "agreeableness1",
            "text": "I am helpful and unselfish with others.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "agreeableness2",
            "text": "I have a good relationship with my neighbors.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "neuroticism1",
            "text": "I often feel sad.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
        {
            "id": "neuroticism2",
            "text": "I get stressed out easily.",
            "type": "select",
            "options": ["1 - Strongly disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly agree"]
        },
    ],
    "health": [
        {
            "id": "health1",
            "text": "How often do you exercise?",
            "type": "select",
            "options": ["Never", "Rarely", "1-2 times a week", "3-4 times a week", "5 or more times a week"]
        },
        {
            "id": "health2",
            "text": "Do you have any dietary restrictions?",
            "type": "select",
            "options": ["None", "Vegetarian", "Vegan", "Gluten-free", "Lactose-free", "Other"]
        },
        {
            "id": "health3",
            "text": "On a scale of 1-5, how would you rate your overall health?",
            "type": "select",
            "options": ["1 - Poor", "2 - Fair", "3 - Good", "4 - Very good", "5 - Excellent"]
        },
        {
            "id": "health4",
            "text": "Do you smoke?",
            "type": "select",
            "options": ["Yes", "No", "Occasionally"]
        },
        {
            "id": "health5",
            "text": "How many hours of sleep do you get on average per night?",
            "type": "select",
            "options": ["Less than 5", "5-6", "7-8", "9-10", "More than 10"]
        },
        {
            "id": "health6",
            "text": "Do you have any chronic health conditions?",
            "type": "text"
        },
        {
            "id": "health7",
            "text": "How often do you consume alcohol?",
            "type": "select",
            "options": ["Never", "Rarely", "Socially", "Moderately", "Frequently"]
        },
        {
            "id": "health8",
            "text": "Do you regularly take any vitamins or supplements?",
            "type": "select",
            "options": ["Yes", "No"]
        },
        {
            "id": "health9",
            "text": "How often do you eat fast food?",
            "type": "select",
            "options": ["Never", "Once a month", "2-3 times a month", "Once a week", "Multiple times a week"]
        },
        {
            "id": "health10",
            "text": "Do you participate in any mindfulness practices, such as meditation or yoga?",
            "type": "select",
            "options": ["Yes", "No"]
        },
        {
            "id": "health11",
            "text": "On a scale of 1-5, how would you rate your stress levels?",
            "type": "select",
            "options": ["1 - Very low", "2 - Low", "3 - Moderate", "4 - High", "5 - Very high"]
        },
        {
            "id": "health12",
            "text": "Have you had a routine medical checkup within the last year?",
            "type": "select",
            "options": ["Yes", "No"]
        }
    ],
    "family": [
        {
            "id": "family1",
            "text": "Are you married or in a relationship?",
            "type": "select",
            "options": ["Single", "In a relationship", "Married", "Divorced", "Widowed"]
        },
        {
            "id": "family2",
            "text": "Do you have children?",
            "type": "select",
            "options": ["Yes", "No"]
        },
        {
            "id": "family3",
            "text": "If you have children, how many do you have?",
            "type": "number"
        },
        {
            "id": "family4",
            "text": "How would you describe your relationship with your immediate family?",
            "type": "select",
            "options": ["Very close", "Close", "Neutral", "Distant", "Very distant"]
        },
        {
            "id": "family5",
            "text": "Do you live with any family members?",
            "type": "select",
            "options": ["Yes", "No"]
        },
        {
            "id": "family6",
            "text": "How often do you communicate with your extended family?",
            "type": "select",
            "options": ["Daily", "Weekly", "Monthly", "A few times a year", "Rarely or never"]
        },
        {
            "id": "family7",
            "text": "Do you have any siblings?",
            "type": "select",
            "options": ["Yes", "No"]
        },
        {
            "id": "family8",
            "text": "If you have siblings, how many do you have?",
            "type": "number"
        },
        {
            "id": "family9",
            "text": "How would you describe your relationship with your siblings?",
            "type": "select",
            "options": ["Very close", "Close", "Neutral", "Distant", "Very distant"]
        },
        {
            "id": "family10",
            "text": "How often do you participate in family gatherings or events?",
            "type": "select",
            "options": ["Weekly", "Monthly", "A few times a year", "Annually", "Rarely or never"]
        },
        {
            "id": "family11",
            "text": "How important is maintaining family traditions to you?",
            "type": "select",
            "options": ["Very important", "Important", "Neutral", "Not very important", "Not important at all"]
        },
        {
            "id": "family12",
            "text": "Do you provide care or support for any family members?",
            "type": "select",
            "options": ["Yes", "No"]
        }
    ],
    "work": [
        {
            "id": "work1",
            "text": "What is your current occupation?"
        },
        {
            "id": "work2",
            "text": "Are you satisfied with your current job?"
        },
        # Add more work questions as needed
    ],
}
