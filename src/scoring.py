from metrics import salutation_level, keyword_presence, flow_score, filler_word_score
from sentiment_analysis import sentiment_score

def compute_score(text):
    stats = {}
    stats["salutation"] = salutation_level(text)
    must, good = keyword_presence(text)
    stats["keywords_score"] = must * 4 + good * 2
    stats["flow_score"] = flow_score()
    stats["filler_score"] = filler_word_score(text)
    stats["sentiment"] = sentiment_score(text) * 15  # scale 0-15
    overall = stats["salutation"] + stats["keywords_score"] + stats["flow_score"] + stats["filler_score"] + stats["sentiment"]
    stats["overall_score"] = round(overall, 2)
    return stats
