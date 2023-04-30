from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "normal_range",
                      "minor": "normal_range"}
    regex_rules = [
        re.compile(r'(?i)\bnormal[ -]range\b'),
    ]
    string_matches = [  # keep for testing regex
        "normal range",
    ]

