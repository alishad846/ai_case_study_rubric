import re

FILLER_WORDS = ["um", "uh", "like", "you know", "so", "actually", "basically",
                "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"]

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def count_filler_words(text):
    text_lower = text.lower()
    return sum(text_lower.count(word) for word in FILLER_WORDS)
