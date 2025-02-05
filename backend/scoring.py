import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

nltk.download("punkt")

def evaluate_fluency(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    sentence_count = len(sentences)
    word_count = len(words)
    
    avg_sentence_length = word_count / max(sentence_count, 1)
    fluency_score = 10 - abs(avg_sentence_length - 15)  # Ideal: 15 words per sentence
    return max(0, min(10, fluency_score))

def evaluate_vocabulary(text):
    words = word_tokenize(text)
    word_freq = Counter(words)
    unique_words = len(word_freq.keys())

    vocab_score = min(10, unique_words / len(words) * 10)  # More unique words = better score
    return max(0, vocab_score)

def evaluate_grammar(text):
    grammar_errors = sum(1 for word in text.split() if word.endswith("ed") and "was" in text)  # Simple rule
    grammar_score = 10 - grammar_errors
    return max(0, min(10, grammar_score))

def evaluate_pronunciation(text):
    mispronounced_words = sum(1 for word in text.split() if word in ["aks", "gonna", "wanna"])  # Simple placeholder
    pronunciation_score = 10 - mispronounced_words
    return max(0, min(10, pronunciation_score))

def calculate_ielts_score(transcription):
    fluency = evaluate_fluency(transcription)
    vocabulary = evaluate_vocabulary(transcription)
    grammar = evaluate_grammar(transcription)
    pronunciation = evaluate_pronunciation(transcription)

    final_score = (fluency + vocabulary + grammar + pronunciation) / 4
    return {
        "fluency": round(fluency, 1),
        "vocabulary": round(vocabulary, 1),
        "grammar": round(grammar, 1),
        "pronunciation": round(pronunciation, 1),
        "final_score": round(final_score, 1),
    }