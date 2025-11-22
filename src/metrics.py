from text_preprocessing import text_stats
from utils import count_filler_words

SALUTATIONS = {
    "no": 0,
    "normal": 2,
    "good": 4,
    "excellent": 5
}

KEYWORDS_MUST_HAVE = ["name", "age", "class", "school", "family", "hobbies", "goal", "unique"]
KEYWORDS_GOOD_TO_HAVE = ["origin", "ambition", "fun fact", "strength"]

def salutation_level(text):
    text_lower = text.lower()
    if "i am excited" in text_lower or "feeling great" in text_lower:
        return SALUTATIONS["excellent"]
    elif any(x in text_lower for x in ["good morning", "good afternoon", "good evening", "good day", "hello everyone"]):
        return SALUTATIONS["good"]
    elif any(x in text_lower for x in ["hi", "hello"]):
        return SALUTATIONS["normal"]
    else:
        return SALUTATIONS["no"]

def keyword_presence(text):
    text_lower = text.lower()
    must_have_count = sum(1 for kw in KEYWORDS_MUST_HAVE if kw in text_lower)
    good_count = sum(1 for kw in KEYWORDS_GOOD_TO_HAVE if kw in text_lower)
    return must_have_count, good_count

def flow_score():
    # For simplicity, assume order followed
    return 5

def filler_word_score(text):
    total_words = len(text.split())
    filler_count = count_filler_words(text)
    rate = (filler_count / total_words) * 100
    if rate <= 3: return 15
    elif rate <= 6: return 12
    elif rate <= 9: return 9
    elif rate <= 12: return 6
    else: return 3
