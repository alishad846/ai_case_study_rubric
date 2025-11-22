import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        duration_sec = len(audio.frame_data) / (audio.sample_rate * audio.sample_width)
        return text, duration_sec
    except Exception as e:
        return "", 0
