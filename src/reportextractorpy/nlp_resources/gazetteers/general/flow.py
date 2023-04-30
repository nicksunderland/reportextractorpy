from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "flow",
                      "minor": "flow"}
    regex_rules = [
        re.compile(r'(?i)\bflow\b'),
    ]
    string_matches = [  # keep for testing regex
        "flow",
    ]
