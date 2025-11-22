import streamlit as st
from scoring import compute_score
from text_preprocessing import text_stats
from audio_processing import transcribe_audio
import pandas as pd
import plotly.express as px
import json

st.title("AI Case Study Rubric Evaluator")

input_type = st.radio("Choose input type", ["Text", "Audio"])

if input_type == "Text":
    user_text = st.text_area("Paste your transcript here:")
    if st.button("Analyze"):
        if user_text.strip():
            stats = text_stats(user_text)
            scores = compute_score(user_text)
            st.subheader("Transcript Analysis")
            st.write(f"Word count: {stats['word_count']}, Sentence count: {stats['sentence_count']}")

            st.subheader("Rubric Scores")
            st.json(scores)

            # Prepare data for chart
            criteria_scores = {
                "Salutation": scores["salutation"],
                "Keywords": scores["keywords_score"],
                "Flow": scores["flow_score"],
                "Filler Word Penalty": scores["filler_score"],
                "Engagement": scores["sentiment"]
            }
            df = pd.DataFrame({"Criteria": list(criteria_scores.keys()), "Score": list(criteria_scores.values())})

            st.bar_chart(df.set_index("Criteria"))
            
            # Radar chart using Plotly
            fig = px.line_polar(df, r='Score', theta='Criteria', line_close=True)
            st.plotly_chart(fig, use_container_width=True)

else:
    uploaded_file = st.file_uploader("Upload audio file (wav, mp3)", type=["wav", "mp3"])
    if uploaded_file is not None:
        st.audio(uploaded_file)
        text, duration_sec = transcribe_audio(uploaded_file)
        st.write(f"Transcript: {text}")
        stats = text_stats(text)
        scores = compute_score(text)
        scores["duration_sec"] = duration_sec

        st.subheader("Transcript Analysis")
        st.write(f"Word count: {stats['word_count']}, Sentence count: {stats['sentence_count']}, Duration: {round(duration_sec,2)} sec")

        st.subheader("Rubric Scores")
        st.json(scores)

        # Bar chart
        criteria_scores = {
            "Salutation": scores["salutation"],
            "Keywords": scores["keywords_score"],
            "Flow": scores["flow_score"],
            "Filler Word Penalty": scores["filler_score"],
            "Engagement": scores["sentiment"]
        }
        df = pd.DataFrame({"Criteria": list(criteria_scores.keys()), "Score": list(criteria_scores.values())})
        st.bar_chart(df.set_index("Criteria"))

        # Radar chart
        fig = px.line_polar(df, r='Score', theta='Criteria', line_close=True)
        st.plotly_chart(fig, use_container_width=True)
