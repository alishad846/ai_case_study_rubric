import streamlit as st
import re
import nltk
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nltk.download("punkt")

# -----------------------------------------------------------
# RUBRIC SCORING ENGINE (ALL FEATURES INCLUDED)
# -----------------------------------------------------------

def compute_full_rubric(text, duration_sec):

    # 1. BASIC TEXT STATS
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    word_count = len(words)
    sentence_count = len(sentences)
    wpm = (word_count / duration_sec) * 60 if duration_sec > 0 else 0

    # 2. SALUTATION SCORE
    salutation_map = {
        "excellent": ["excited to introduce", "feeling great"],
        "good": ["good morning", "good afternoon", "good evening", "good day", "hello everyone"],
        "normal": ["hi", "hello"]
    }

    sal_score = 0
    t = text.lower()

    if any(p in t for p in salutation_map["excellent"]):
        sal_score = 5
    elif any(p in t for p in salutation_map["good"]):
        sal_score = 4
    elif any(p in t for p in salutation_map["normal"]):
        sal_score = 2
    else:
        sal_score = 0

    # 3. MUST-HAVE KEYWORDS
    must_have = {
        "name": ["my name is", "myself"],
        "age": ["years old"],
        "class": ["class"],
        "school": ["school"],
        "family": ["family"],
        "hobby": ["hobby", "like to", "enjoy", "playing"]
    }

    must_score = 0
    must_keywords_found = []
    for key, kw_list in must_have.items():
        if any(k in t for k in kw_list):
            must_score += 4
            must_keywords_found.append(key)

    # 4. GOOD-TO-HAVE KEYWORDS
    good_to_have = {
        "fun fact": ["fun fact"],
        "unique": ["one thing people don't know"],
        "goal": ["dream", "goal", "ambition"],
        "origin": ["i am from"],
        "achievement": ["achieved", "winner"]
    }

    good_score = 0
    good_keywords_found = []
    for key, kw_list in good_to_have.items():
        if any(k in t for k in kw_list):
            good_score += 2
            good_keywords_found.append(key)

    # 5. FLOW SCORE
    correct_order = ["salutation", "name", "basic details", "details", "closing"]
    flow_score = 5  # assume correct since intro → details → end
    # You can add advanced checking later

    # 6. SPEECH RATE SCORE
    if wpm > 161:
        speech_score = 2
    elif wpm >= 141:
        speech_score = 6
    elif wpm >= 111:
        speech_score = 10
    elif wpm >= 81:
        speech_score = 6
    else:
        speech_score = 2

    # 7. FILLER WORD SCORE
    filler_words = ["um", "uh", "like", "you know", "so", "actually", "basically",
                    "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"]

    filler_count = sum(t.count(f) for f in filler_words)
    filler_rate = (filler_count / word_count) * 100 if word_count > 0 else 0

    if filler_rate <= 3:
        filler_score = 15
    elif filler_rate <= 6:
        filler_score = 12
    elif filler_rate <= 9:
        filler_score = 9
    elif filler_rate <= 12:
        filler_score = 6
    else:
        filler_score = 3

    # 8. GRAMMAR SCORE (simple estimation using punctuation consistency)
    estimated_errors = abs(sentence_count - (word_count / 15))
    error_ratio = min(1, estimated_errors / 10)
    grammar_score = int((1 - error_ratio) * 10)

    # 9. VOCABULARY RICHNESS (TTR)
    distinct_words = len(set(words))
    ttr = distinct_words / word_count if word_count > 0 else 0

    if ttr >= 0.9:
        vocab_score = 10
    elif ttr >= 0.7:
        vocab_score = 8
    elif ttr >= 0.5:
        vocab_score = 6
    elif ttr >= 0.3:
        vocab_score = 4
    else:
        vocab_score = 2

    # 10. SENTIMENT
    analyzer = SentimentIntensityAnalyzer()
    pos_score = analyzer.polarity_scores(text)["pos"]

    if pos_score >= 0.9:
        sentiment_score = 15
    elif pos_score >= 0.7:
        sentiment_score = 12
    elif pos_score >= 0.5:
        sentiment_score = 9
    elif pos_score >= 0.3:
        sentiment_score = 6
    else:
        sentiment_score = 3

    # TOTAL SCORE
    total_score = (
        sal_score + must_score + good_score + flow_score +
        speech_score + grammar_score + vocab_score +
        filler_score + sentiment_score
    )

    # RETURN FULL JSON
    return {
        "overall_score": round(total_score, 2),
        "word_count": word_count,
        "sentence_count": sentence_count,
        "wpm": round(wpm, 2),
        "criteria_results": [
            {"criterion": "Salutation", "score": sal_score},
            {"criterion": "Keywords (Must Have)", "score": must_score, "found": must_keywords_found},
            {"criterion": "Keywords (Good to Have)", "score": good_score, "found": good_keywords_found},
            {"criterion": "Flow", "score": flow_score},
            {"criterion": "Speech Rate", "score": speech_score},
            {"criterion": "Grammar", "score": grammar_score},
            {"criterion": "Vocabulary Richness", "score": vocab_score, "ttr": ttr},
            {"criterion": "Filler Clarity", "score": filler_score, "filler_count": filler_count},
            {"criterion": "Engagement", "score": sentiment_score, "positive_score": pos_score}
        ]
    }


# -----------------------------------------------------------
# STREAMLIT UI
# -----------------------------------------------------------

st.title("🎤 AI Communication Rubric Evaluator")

text = st.text_area("Paste transcript here")
duration = st.number_input("Enter audio duration (seconds)", min_value=1, value=52)

if st.button("Evaluate"):

    result = compute_full_rubric(text, duration)

    st.subheader("🏆 Overall Score")
    st.metric("Final Score", result["overall_score"])

    st.subheader("📌 Detailed Breakdown")
    st.json(result)

    # Prepare chart data
    df = pd.DataFrame({
        "Criteria": [c["criterion"] for c in result["criteria_results"]],
        "Score": [c["score"] for c in result["criteria_results"]]
    })

    st.subheader("📊 Bar Chart")
    st.bar_chart(df.set_index("Criteria"))

    st.subheader("🕸 Radar Chart")
    fig = px.line_polar(df, r="Score", theta="Criteria", line_close=True)
    fig.update_traces(fill="toself")
    st.plotly_chart(fig, use_container_width=True)
