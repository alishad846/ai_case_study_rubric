from utils import clean_text
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize

def text_stats(text):
    text = clean_text(text)
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    word_count = len(words)
    sentence_count = len(sentences)
    return {"word_count": word_count, "sentence_count": sentence_count, "words": words, "sentences": sentences}
