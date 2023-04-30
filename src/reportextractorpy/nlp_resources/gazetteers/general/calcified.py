from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Categorical"
    annot_features = {"major": "calcification",
                      "minor": "calcified"}
    regex_rules = [
        re.compile(r'(?i)\b(?<!non-)calcifi(?:cation|ed)\b'),
    ]
    string_matches = [  # keep for testing regex
        "noncalcified",
        "non-calcified"
    ]
