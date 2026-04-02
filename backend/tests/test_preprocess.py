import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.preprocess import (
    clean_text,
    remove_stopwords,
    extract_keywords,
    compute_risk_score,
    detect_language,
)


def test_clean_text_removes_urls():
    text = "check this http://malware.com site out"
    result = clean_text(text)
    assert "http" not in result


def test_clean_text_lowercases():
    text = "RANSOMWARE Attack DETECTED"
    result = clean_text(text)
    assert result == result.lower()


def test_clean_text_removes_special_chars():
    text = "hello!!! world@#$"
    result = clean_text(text)
    assert "!" not in result
    assert "@" not in result


def test_remove_stopwords_removes_common_words():
    text = "the quick brown fox is running"
    result = remove_stopwords(text)
    assert "the" not in result.split()
    assert "is" not in result.split()


def test_extract_keywords_finds_threats():
    text = "selling ransomware and malware tools"
    keywords = extract_keywords(text)
    assert "ransomware" in keywords
    assert "malware" in keywords


def test_extract_keywords_empty_text():
    result = extract_keywords("")
    assert result == []


def test_compute_risk_score_empty():
    score = compute_risk_score([])
    assert score == 0.0


def test_compute_risk_score_with_keywords():
    score = compute_risk_score(["ransomware", "malware", "leak"])
    assert score > 0.0
    assert score <= 1.0


def test_compute_risk_score_anomaly_boost():
    score_normal = compute_risk_score(["ransomware"], is_anomaly=False)
    score_anomaly = compute_risk_score(["ransomware"], is_anomaly=True)
    assert score_anomaly >= score_normal


def test_detect_language_english():
    result = detect_language("this is a normal english sentence about malware")
    assert result == "en"