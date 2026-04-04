import os
import json
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from app.core.logger import get_logger

logger = get_logger(__name__)

THREAT_LABELS = [
    "credential_leak",
    "ransomware",
    "zero_day",
    "malware_sale",
    "unknown"
]

KEYWORD_LABEL_MAP = {
    "credential":      "credential_leak",
    "leak":            "credential_leak",
    "dump":            "credential_leak",
    "breach":          "credential_leak",
    "ransomware":      "ransomware",
    "ransom":          "ransomware",
    "encrypt":         "ransomware",
    "zero-day":        "zero_day",
    "zeroday":         "zero_day",
    "cve":             "zero_day",
    "vulnerability":   "zero_day",
    "exploit":         "zero_day",
    "malware":         "malware_sale",
    "trojan":          "malware_sale",
    "rat":             "malware_sale",
    "keylogger":       "malware_sale",
    "backdoor":        "malware_sale",
    "stealer":         "malware_sale",
}


def assign_label_from_keywords(keywords_str):
    if not keywords_str or str(keywords_str).strip() == "" or str(keywords_str) == "nan":
        return "unknown"
    keywords_str = str(keywords_str)
    keywords = keywords_str.split(",")
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword in KEYWORD_LABEL_MAP:
            return KEYWORD_LABEL_MAP[keyword]
    return "unknown"


def prepare_training_data(df):
    logger.info("Preparing training data...")
    df["label"] = df["keywords"].apply(assign_label_from_keywords)
    label_counts = df["label"].value_counts()
    logger.info("Label distribution:")
    for label, count in label_counts.items():
        logger.info("  " + label + ": " + str(count))
    return df


def train_classifier(df):
    logger.info("Training TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
    )

    X = vectorizer.fit_transform(df["cleaned_text"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    logger.info("Training Random Forest classifier...")
    clf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    report_dict = classification_report(y_test, y_pred, output_dict=True)

    logger.info("Classification Report:\n" + classification_report(y_test, y_pred))

    classes = []
    for label, metrics in report_dict.items():
        if label in ["accuracy", "macro avg", "weighted avg"]:
            continue
        classes.append({
            "name": label,
            "precision": round(metrics["precision"], 4),
            "recall": round(metrics["recall"], 4),
            "f1": round(metrics["f1-score"], 4),
            "support": int(metrics["support"]),
        })

    result = {
        "accuracy": round(report_dict["accuracy"], 4),
        "macro_avg": {
            "precision": round(report_dict["macro avg"]["precision"], 4),
            "recall": round(report_dict["macro avg"]["recall"], 4),
            "f1": round(report_dict["macro avg"]["f1-score"], 4),
        },
        "weighted_avg": {
            "precision": round(report_dict["weighted avg"]["precision"], 4),
            "recall": round(report_dict["weighted avg"]["recall"], 4),
            "f1": round(report_dict["weighted avg"]["f1-score"], 4),
        },
        "classes": classes,
    }

    os.makedirs("data/models/classifier", exist_ok=True)
    with open("data/models/classifier/classifier_report.json", "w") as f:
        json.dump(result, f, indent=2)
    logger.info("Saved classifier report to data/models/classifier/classifier_report.json")

    return clf, vectorizer


def predict_threat_type(clf, vectorizer, text):
    vec = vectorizer.transform([text])
    prediction = clf.predict(vec)[0]
    probabilities = clf.predict_proba(vec)[0]
    confidence = round(max(probabilities), 4)
    return prediction, confidence


def save_classifier(clf, vectorizer, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "classifier.pkl"), "wb") as f:
        pickle.dump(clf, f)
    with open(os.path.join(output_dir, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    logger.info("Saved classifier and vectorizer to " + output_dir)


def load_classifier(output_dir):
    with open(os.path.join(output_dir, "classifier.pkl"), "rb") as f:
        clf = pickle.load(f)
    with open(os.path.join(output_dir, "vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)
    logger.info("Loaded classifier from " + output_dir)
    return clf, vectorizer


def run_classification(cleaned_data_path, model_output_dir):
    df = pd.read_csv(cleaned_data_path)
    df = df.dropna(subset=["cleaned_text"])
    df = prepare_training_data(df)
    clf, vectorizer = train_classifier(df)
    save_classifier(clf, vectorizer, model_output_dir)
    df["threat_type"] = clf.predict(vectorizer.transform(df["cleaned_text"]))
    df.to_csv(cleaned_data_path, index=False)
    logger.info("Saved threat_type back to " + cleaned_data_path)
    return clf, vectorizer, df


def save_classification_report(clf, vectorizer, df, output_dir):
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split

    X = vectorizer.transform(df["cleaned_text"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    y_pred = clf.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)

    classes = []
    for label, metrics in report.items():
        if label in ["accuracy", "macro avg", "weighted avg"]:
            continue
        classes.append({
            "name": label,
            "precision": round(metrics["precision"], 4),
            "recall": round(metrics["recall"], 4),
            "f1": round(metrics["f1-score"], 4),
            "support": int(metrics["support"]),
        })

    result = {
        "accuracy": round(report["accuracy"], 4),
        "macro_avg": {
            "precision": round(report["macro avg"]["precision"], 4),
            "recall": round(report["macro avg"]["recall"], 4),
            "f1": round(report["macro avg"]["f1-score"], 4),
        },
        "weighted_avg": {
            "precision": round(report["weighted avg"]["precision"], 4),
            "recall": round(report["weighted avg"]["recall"], 4),
            "f1": round(report["weighted avg"]["f1-score"], 4),
        },
        "classes": classes,
    }

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "classifier_report.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    logger.info("Saved classification report to " + output_path)
    return result

if __name__ == "__main__":
    run_classification(
        cleaned_data_path="data/processed/clean_posts.csv",
        model_output_dir="data/models/classifier"
    )