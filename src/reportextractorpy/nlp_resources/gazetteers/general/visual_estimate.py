from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "visual_estimate",
                      "minor": "visual_estimate"}
    regex_rules = [
        re.compile(r'(?i)\bvisual(?:ly)?\b'),
    ]
    string_matches = [  # keep for testing regex
        "visually",
    ]
