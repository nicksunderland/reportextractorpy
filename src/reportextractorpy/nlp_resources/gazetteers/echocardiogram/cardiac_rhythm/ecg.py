from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "ecg",
                      "minor": "ecg"}
    regex_rules = [
        re.compile(r'(?i)\b12[- ]?lead(?: ECG)?|ECG\b'),
    ]
    string_matches = [
        "ECG",
        "ecg",
        "12-lead",
        "12 lead",
        "12-lead ECG",
        "12 lead ECG",
        "12-lead ecg",
        "12 lead ecg"
    ]
