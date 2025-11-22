📘 AI Communication Rubric Evaluator

A Streamlit-based application that evaluates student self-introduction transcripts using a rubric. The tool analyzes text or audio, detects required details (name, age, class, hobbies, etc.), checks flow & structure, sentiment, filler words, and produces a detailed score (0–100) with JSON output.

🚀 Features
✓ Supports Text & Audio Input

Paste transcript directly

Upload audio (wav/mp3) → Automatic speech-to-text

✓ Rubric-Based Scoring (0–100)

The tool scores:

Salutation Level

Keyword Presence (must-have & good-to-have)

Flow / Structure

Filler Word Penalty

Engagement / Sentiment

Vocabulary & Grammar (basic checks)

✓ NLP-Powered Analysis

Word & sentence count

Filler word detection

Sentiment using TextBlob + VADER

Scoring logic matches rubric provided in case study

✓ JSON Report Output

Produces a clean JSON result containing:

Overall Score

Word/Sentence Count

Per-Criterion Scores

Detected keywords

✓ Visual Charts

Bar Chart

Radar Chart
(Helps visualize strengths and weaknesses)

🧠 Tech Stack
Frontend

Streamlit → clean, interactive UI

Plotly → bar chart + radar chart visualizations

Backend / NLP

Python 3.12

NLTK → tokenization

TextBlob → sentiment polarity

VADER → positivity scoring

Sentence-Transformers → semantic understanding (optional)

SpeechRecognition → audio transcription

pydub → audio processing

Utilities

JSON output

Modular architecture (scoring, metrics, text processing, audio processing)

📂 Project Structure
ai_case_study/
│
├── src/
│   ├── app.py                 # Streamlit frontend
│   ├── main.py                # CLI script for transcripts
│   ├── scoring.py             # Rubric scoring logic
│   ├── metrics.py             # Word count, filler words, etc.
│   ├── sentiment_analysis.py  # Sentiment scoring
│   ├── text_processing.py     # NLP preprocessing
│   ├── audio_processing.py    # Audio → text + WPM
│   └── utils.py               # Common helper methods
│
├── reports/
│   └── output.json            # Saved evaluation
│
└── requirements.txt

▶️ How to Run Locally
1. Clone the repo
git clone https://github.com/<your-username>/ai_case_study_rubric.git
cd ai_case_study_rubric

2. Create venv
python -m venv venv
.\venv\Scripts\activate

3. Install requirements
pip install -r requirements.txt

4. Download tokenizer (only once)
python -c "import nltk; nltk.download('punkt')"

5. Run Streamlit App
streamlit run src/app.py

📝 Output Example (JSON)
{
  "overall_score": 49.53,
  "word_count": 134,
  "sentence_count": 11,
  "criteria_results": [
    { "criterion": "Basic Details", "score": 10 },
    { "criterion": "Personal Insights", "score": 16.67 },
    { "criterion": "Communication Quality", "score": 0 },
    { "criterion": "Flow", "score": 5 },
    { "criterion": "Filler Word Penalty", "score": 15 },
    { "criterion": "Engagement", "score": 2.87 }
  ]
}

📄 Case Study Purpose

This project is built for the Nirmaan Education AI Internship case study.
It demonstrates:

Product thinking

Practical NLP implementation

Clear UI + JSON output

Modular, scalable code design

🙌 Contributions

Pull requests are welcome!