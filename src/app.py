import streamlit as st
import nltk
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import pandas as pd
import plotly.express as px

nltk.download("punkt")

# ------------------------------------------------------------------
# FULL RUBRIC SCORING ENGINE
# ------------------------------------------------------------------

def compute_rubric(text, duration_sec=None):
    text_low = text.lower()

    # WORDS & SENTENCES
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)

    word_count = len(words)
    sentence_count = len(sentences)

    # ---- Speech Rate Logic ----
    if duration_sec is None:
        # NO DURATION → assume average speaking rate 120 WPM
        wpm = 120
    else:
        # AUDIO MODE → real duration
        wpm = (word_count / duration_sec) * 60 if duration_sec > 0 else 0

    # ---------------- SALUTATION ----------------
    sal_score = 0
    if any(x in text_low for x in ["excited to", "feeling great"]):
        sal_score = 5
    elif "hello everyone" in text_low or any(x in text_low for x in ["good morning", "good afternoon", "good evening"]):
        sal_score = 4
    elif any(x in text_low for x in ["hi", "hello"]):
        sal_score = 2

    # ---------------- MUST-HAVE KEYWORDS -----------
    must_map = {
        "name": ["my name is", "myself"],
        "age": ["years old"],
        "class": ["class"],
        "school": ["school"],
        "family": ["family"],
        "hobby": ["hobby", "playing", "enjoy"]
    }

    must_score = 0
    must_found = []
    for key, kws in must_map.items():
        if any(k in text_low for k in kws):
            must_score += 4
            must_found.append(key)

    # ---------------- GOOD-TO-HAVE KEYWORDS --------
    good_map = {
        "fun fact": ["fun fact"],
        "unique": ["one thing people"],
        "goal": ["goal", "dream", "ambition"],
        "origin": ["i am from"],
        "achievement": ["achieve", "winner"]
    }

    good_score = 0
    good_found = []
    for key, kws in good_map.items():
        if any(k in text_low for k in kws):
            good_score += 2
            good_found.append(key)

    # ---------------- FLOW SCORE ----------------
    flow_score = 5  # assume correct order

    # ---------------- SPEECH RATE SCORE ----------------
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

    # ---------------- FILLER WORDS ----------------
    filler_words = ["um", "uh", "like", "you know", "so", "actually", "basically", "right"]
    filler_count = sum(text_low.count(f) for f in filler_words)
    filler_rate = (filler_count / word_count * 100) if word_count else 0

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

    # ---------------- GRAMMAR SCORE ----------------
    estimated_errors = abs(sentence_count - (word_count / 15))
    grammar_score = max(2, min(10, int(10 - estimated_errors)))  # safe bound

    # ---------------- VOCAB TTR ----------------
    distinct = len(set(words))
    ttr = distinct / word_count if word_count else 0

    if ttr >= 0.9: vocab_score = 10
    elif ttr >= 0.7: vocab_score = 8
    elif ttr >= 0.5: vocab_score = 6
    elif ttr >= 0.3: vocab_score = 4
    else: vocab_score = 2

    # ---------------- SENTIMENT ----------------
    analyzer = SentimentIntensityAnalyzer()
    pos_score = analyzer.polarity_scores(text)["pos"]

    if pos_score >= 0.9: senti_score = 15
    elif pos_score >= 0.7: senti_score = 12
    elif pos_score >= 0.5: senti_score = 9
    elif pos_score >= 0.3: senti_score = 6
    else: senti_score = 3

    # ---------------- TOTAL ----------------
    total_score = (
        sal_score + must_score + good_score + flow_score +
        speech_score + grammar_score + vocab_score +
        filler_score + senti_score
    )

    return {
        "overall_score": total_score,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "wpm": round(wpm, 2),
        "criteria_results": [
            {"criterion": "Salutation", "score": sal_score},
            {"criterion": "Keywords (Must Have)", "score": must_score, "found": must_found},
            {"criterion": "Keywords (Good to Have)", "score": good_score, "found": good_found},
            {"criterion": "Flow", "score": flow_score},
            {"criterion": "Speech Rate", "score": speech_score},
            {"criterion": "Grammar", "score": grammar_score},
            {"criterion": "Vocabulary TTR", "score": vocab_score},
            {"criterion": "Filler Words", "score": filler_score, "filler_count": filler_count},
            {"criterion": "Engagement (Sentiment)", "score": senti_score}
        ]
    }

# ------------------------------------------------------------------
# AUDIO SPEECH RECOGNITION
# ------------------------------------------------------------------

def transcribe_audio(uploaded_file):
    audio = AudioSegment.from_file(uploaded_file)
    duration_sec = len(audio) / 1000

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio.export(tmp.name, format="wav")
        wav_path = tmp.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    return text, duration_sec

# ------------------------------------------------------------------
# STREAMLIT UI
# ------------------------------------------------------------------

st.title("🎤 AI Communication Rubric Evaluator")

mode = st.radio("Choose Input Type", ["Text", "Audio"])

# ===================== TEXT MODE ======================
if mode == "Text":
    text_input = st.text_area("Paste transcript here...")

    if st.button("Evaluate Text"):
        if text_input.strip() == "":
            st.error("Please enter a transcript!")
        else:
            result = compute_rubric(text_input)

            st.subheader("🧾 Full JSON Output")
            st.json(result)

            # CHARTS
            df = pd.DataFrame({
                "Criteria": [c["criterion"] for c in result["criteria_results"]],
                "Score": [c["score"] for c in result["criteria_results"]],
            })

            st.subheader("📊 Bar Chart")
            bar = px.bar(df, x="Criteria", y="Score", text="Score")
            st.plotly_chart(bar)

            st.subheader("🕸 Radar Chart")
            radar = px.line_polar(df, r="Score", theta="Criteria", line_close=True)
            radar.update_traces(fill="toself")
            st.plotly_chart(radar)

# ===================== AUDIO MODE ======================
else:
    uploaded = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])

    if uploaded:
        st.audio(uploaded)

        text, duration = transcribe_audio(uploaded)
        st.write("### Transcription:")
        st.info(text)

        result = compute_rubric(text, duration)

        st.json(result)

        df = pd.DataFrame({
            "Criteria": [c["criterion"] for c in result["criteria_results"]],
            "Score": [c["score"] for c in result["criteria_results"]],
        })

        st.subheader("📊 Bar Chart")
        bar = px.bar(df, x="Criteria", y="Score", text="Score")
        st.plotly_chart(bar)

        st.subheader("🕸 Radar Chart")
        radar = px.line_polar(df, r="Score", theta="Criteria", line_close=True)
        radar.update_traces(fill="toself")
        st.plotly_chart(radar)
