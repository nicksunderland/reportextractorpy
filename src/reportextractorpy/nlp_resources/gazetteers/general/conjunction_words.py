from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "grammar",
                      "minor": "conjunction"}
    regex_rules = [
        re.compile(r'(?i)\b(?:and|n?or|both|however)\b'),
    ]
    string_matches = [  # keep for testing regex
        "and",
        "nor",
        "both"
        "or",
        "however"
    ]
