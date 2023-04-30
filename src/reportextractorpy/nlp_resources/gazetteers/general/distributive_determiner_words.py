from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "grammar",
                      "minor": "distributive_determiner"}
    regex_rules = [
        re.compile(r'(?i)\b(?:n?either|both|each|all)\b'),
    ]
    string_matches = [  # keep for testing regex
        "both",
        "each",
        "all",
        "either",
        "neither"
    ]
