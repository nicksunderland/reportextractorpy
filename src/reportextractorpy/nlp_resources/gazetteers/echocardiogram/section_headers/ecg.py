from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "ecg"}
    regex_rules = [
        re.compile(r'ECG ?[:-]{1,2}')
    ]
    string_matches = [  # keep for testing regex
        "ECG:"
    ]

