import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from app.core.logger import get_logger

logger = get_logger(__name__)

CONTAMINATION = 0.05


def train_anomaly_detector(df):
    logger.info("Building TF-IDF matrix for anomaly detection...")
    vectorizer = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        min_df=2,
    )

    X = vectorizer.fit_transform(df["cleaned_text"])

    logger.info("Training Isolation Forest...")
    iso_forest = IsolationForest(
        contamination=CONTAMINATION,
        random_state=42,
        n_jobs=-1,
    )
    iso_forest.fit(X)

    predictions = iso_forest.predict(X)
    scores = iso_forest.decision_function(X)

    df["is_anomaly"] = [True if p == -1 else False for p in predictions]
    df["anomaly_score"] = scores

    anomaly_count = df["is_anomaly"].sum()
    logger.info("Flagged " + str(anomaly_count) + " anomalies out of " + str(len(df)) + " posts")

    return iso_forest, vectorizer, df


def get_top_anomalies(df, top_n=50):
    anomalies = df[df["is_anomaly"] == True].copy()
    anomalies = anomalies.sort_values("anomaly_score")
    return anomalies.head(top_n)


def predict_anomaly(iso_forest, vectorizer, text):
    vec = vectorizer.transform([text])
    prediction = iso_forest.predict(vec)[0]
    score = iso_forest.decision_function(vec)[0]
    is_anomaly = prediction == -1
    return is_anomaly, round(float(score), 4)


def save_anomaly_model(iso_forest, vectorizer, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "isolation_forest.pkl"), "wb") as f:
        pickle.dump(iso_forest, f)
    with open(os.path.join(output_dir, "anomaly_vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    logger.info("Saved anomaly model to " + output_dir)


def load_anomaly_model(output_dir):
    with open(os.path.join(output_dir, "isolation_forest.pkl"), "rb") as f:
        iso_forest = pickle.load(f)
    with open(os.path.join(output_dir, "anomaly_vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)
    logger.info("Loaded anomaly model from " + output_dir)
    return iso_forest, vectorizer


def run_anomaly_detection(cleaned_data_path, model_output_dir):
    df = pd.read_csv(cleaned_data_path)
    df = df.dropna(subset=["cleaned_text"])
    iso_forest, vectorizer, df = train_anomaly_detector(df)
    save_anomaly_model(iso_forest, vectorizer, model_output_dir)
    top_anomalies = get_top_anomalies(df)
    logger.info("Top anomalous posts saved")
    return iso_forest, df, top_anomalies


if __name__ == "__main__":
    run_anomaly_detection(
        cleaned_data_path="data/processed/clean_posts.csv",
        model_output_dir="data/models/anomaly"
    )