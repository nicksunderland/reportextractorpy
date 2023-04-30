from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Categorical"
    annot_features = {"major": "calcification",
                      "minor": "noncalcified"}
    regex_rules = [
        re.compile(r'(?i)\bnon-?calcified\b'),
    ]
    string_matches = [  # keep for testing regex
        "noncalcified",
        "non-calcified"
    ]