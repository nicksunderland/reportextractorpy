from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "age",
                      "minor": "age"}
    regex_rules = [
        re.compile(r'(?i)\b(?:age|years old)\b'),
    ]
    string_matches = [  # keep for testing regex
        "age",
        "years old",
    ]
