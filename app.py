import streamlit as st
from sentence_transformers import SentenceTransformer, util

# Load PyTorch-based model
model = SentenceTransformer('all-MiniLM-L6-v2')

st.title("AI Self-Introduction Scorer")

# Text input
transcript = st.text_area("Paste your transcript here:")

if st.button("Score"):
    if transcript.strip() == "":
        st.warning("Please paste some text!")
    else:
        # Encode transcript
        embedding = model.encode(transcript)

        # Dummy scoring logic for demo (replace with your rubric logic)
        # Here we just show length and some fake score
        word_count = len(transcript.split())
        overall_score = min(100, word_count * 0.5)

        st.write({
            "overall_score": overall_score,
            "word_count": word_count,
            "criteria_results": [
                {"criterion": "Basic Details", "score": 20},
                {"criterion": "Personal Insights", "score": 15},
                {"criterion": "Communication Quality", "score": 12}
            ]
        })
