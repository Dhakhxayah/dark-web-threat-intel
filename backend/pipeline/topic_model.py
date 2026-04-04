import os
import pickle
import pandas as pd
from gensim import corpora, models
from app.core.logger import get_logger

logger = get_logger(__name__)

NUM_TOPICS = 10
PASSES = 15


TOPIC_LABELS = {
    0: "Credential leaks",
    1: "Ransomware campaigns",
    2: "Zero-day exploits",
    3: "Malware sales",
    4: "Botnet activity",
    5: "Phishing kits",
    6: "Data dumps",
    7: "Dark market listings",
    8: "Vulnerability discussion",
    9: "General threat chatter",
}


def load_cleaned_data(file_path):
    logger.info("Loading cleaned data from " + file_path)
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["cleaned_text"])
    return df


def build_corpus(texts):
    logger.info("Building dictionary and corpus...")
    tokenized = [text.split() for text in texts]
    dictionary = corpora.Dictionary(tokenized)
    dictionary.filter_extremes(no_below=5, no_above=0.5)
    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized]
    logger.info("Dictionary size: " + str(len(dictionary)))
    return corpus, dictionary, tokenized


def train_lda(corpus, dictionary):
    logger.info("Training LDA model with " + str(NUM_TOPICS) + " topics...")
    lda_model = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=NUM_TOPICS,
        passes=PASSES,
        random_state=42,
    )
    logger.info("LDA training complete")
    return lda_model


def get_topic_summary(lda_model, num_words=10):
    summaries = []
    for topic_id in range(NUM_TOPICS):
        top_words = [word for word, _ in lda_model.show_topic(topic_id, topn=num_words)]
        summaries.append({
            "topic_id": topic_id,
            "label": TOPIC_LABELS.get(topic_id, "Topic " + str(topic_id)),
            "top_words": top_words,
        })
    return summaries


def assign_topics_to_docs(lda_model, corpus):
    logger.info("Assigning topics to documents...")
    topic_assignments = []
    for doc_bow in corpus:
        topic_distribution = lda_model.get_document_topics(doc_bow)
        if topic_distribution:
            dominant_topic = max(topic_distribution, key=lambda x: x[1])[0]
        else:
            dominant_topic = -1
        topic_assignments.append(dominant_topic)
    return topic_assignments


def save_model(lda_model, dictionary, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    lda_model.save(os.path.join(output_dir, "lda_model"))
    dictionary.save(os.path.join(output_dir, "lda_dictionary"))
    logger.info("Saved LDA model to " + output_dir)


def load_model(output_dir):
    lda_model = models.LdaModel.load(os.path.join(output_dir, "lda_model"))
    dictionary = corpora.Dictionary.load(os.path.join(output_dir, "lda_dictionary"))
    logger.info("Loaded LDA model from " + output_dir)
    return lda_model, dictionary


def run_topic_modeling(cleaned_data_path, model_output_dir):
    df = load_cleaned_data(cleaned_data_path)
    corpus, dictionary, tokenized = build_corpus(df["cleaned_text"].tolist())
    lda_model = train_lda(corpus, dictionary)
    df["dominant_topic"] = assign_topics_to_docs(lda_model, corpus)
    save_model(lda_model, dictionary, model_output_dir)
    df.to_csv(cleaned_data_path, index=False)
    logger.info("Saved dominant_topic back to " + cleaned_data_path)
    summaries = get_topic_summary(lda_model)
    return lda_model, df, summaries

if __name__ == "__main__":
    run_topic_modeling(
        cleaned_data_path="data/processed/clean_posts.csv",
        model_output_dir="data/models/lda"
    )