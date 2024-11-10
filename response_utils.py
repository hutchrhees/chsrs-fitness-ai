# response_utils.py
def goal_synonym_mapping(text):
    synonyms = {
        "fat": "fat loss",
        "weight loss": "fat loss",
        "slimming down": "fat loss",
        "burn fat": "fat loss",
        "shedding pounds": "fat loss",
        "skinny": "fat loss",
        "muscle": "muscle building",
        "strength": "strength building",
        # Add more mappings if needed
    }
    # Replace any goal-related terms in the response
    for word, synonym in synonyms.items():
        if word in text:
            text = text.replace(word, synonym)
    return text
