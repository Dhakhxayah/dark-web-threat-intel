import re
import os
import pandas as pd
import nltk
import spacy
from langdetect import detect
from nltk.corpus import stopwords
from app.core.logger import get_logger

logger = get_logger(__name__)

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

THREAT_KEYWORDS = [
    "ransomware", "malware", "exploit", "zero-day", "credential",
    "leak", "breach", "dump", "botnet", "phishing", "trojan",
    "backdoor", "keylogger", "ddos", "vulnerability", "cve",
    "stealer", "rat", "c2", "command and control", "darknet",
    "tor", "onion", "bitcoin", "monero", "ransom"
]


def load_raw_data(file_path):
    logger.info("Loading raw data from " + file_path)
    df = pd.read_csv(file_path)
    logger.info("Loaded " + str(len(df)) + " rows")
    return df


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def filter_english(df, text_column):
    logger.info("Filtering English posts...")
    df["language"] = df[text_column].apply(detect_language)
    english_df = df[df["language"] == "en"].copy()
    logger.info("Kept " + str(len(english_df)) + " English posts out of " + str(len(df)))
    return english_df


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(text):
    words = text.split()
    filtered = [w for w in words if w not in stop_words]
    return " ".join(filtered)


def lemmatize(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    return " ".join(lemmas)


def extract_keywords(text):
    found = []
    for keyword in THREAT_KEYWORDS:
        if keyword in text:
            found.append(keyword)
    return found


def compute_risk_score(keywords_found, is_anomaly=False):
    base_score = len(keywords_found) / len(THREAT_KEYWORDS)
    if is_anomaly:
        base_score = min(base_score + 0.2, 1.0)
    return round(base_score, 4)


def preprocess_dataframe(df, text_column):
    logger.info("Starting preprocessing pipeline...")

    df = filter_english(df, text_column)

    logger.info("Cleaning text...")
    df["cleaned_text"] = df[text_column].apply(clean_text)

    logger.info("Removing stopwords...")
    df["cleaned_text"] = df["cleaned_text"].apply(remove_stopwords)

    logger.info("Lemmatizing...")
    df["cleaned_text"] = df["cleaned_text"].apply(lemmatize)

    logger.info("Extracting threat keywords...")
    df["keywords"] = df["cleaned_text"].apply(extract_keywords)
    df["keywords"] = df["keywords"].apply(lambda k: ",".join(k))

    logger.info("Computing base risk scores...")
    df["risk_score"] = df["keywords"].apply(
        lambda k: compute_risk_score(k.split(",") if k else [])
    )

    df = df.dropna(subset=["cleaned_text"])
    df = df[df["cleaned_text"].str.strip() != ""]

    logger.info("Preprocessing done. Final rows: " + str(len(df)))
    return df


def save_processed_data(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Saved processed data to " + output_path)


def run_preprocessing(input_path, output_path, text_column="text"):
    df = load_raw_data(input_path)
    df = preprocess_dataframe(df, text_column)
    save_processed_data(df, output_path)
    return df


if __name__ == "__main__":
    run_preprocessing(
        input_path="data/raw/darkdump.csv",
        output_path="data/processed/clean_posts.csv",
        text_column="text"
    )