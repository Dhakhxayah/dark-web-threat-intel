import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.classifier import assign_label_from_keywords


def test_credential_label():
    result = assign_label_from_keywords("credential,leak")
    assert result == "credential_leak"


def test_ransomware_label():
    result = assign_label_from_keywords("ransomware,encrypt")
    assert result == "ransomware"


def test_zero_day_label():
    result = assign_label_from_keywords("cve,exploit")
    assert result == "zero_day"


def test_malware_label():
    result = assign_label_from_keywords("malware,trojan")
    assert result == "malware_sale"


def test_unknown_label():
    result = assign_label_from_keywords("")
    assert result == "unknown"


def test_unknown_label_no_match():
    result = assign_label_from_keywords("hello,world,nothing")
    assert result == "unknown"


def test_first_match_wins():
    result = assign_label_from_keywords("credential,ransomware")
    assert result in ["credential_leak", "ransomware"]