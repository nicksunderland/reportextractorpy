from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "mass",
                      "minor": "g"}
    regex_rules = [
        re.compile(r'grams?|(?<=\d)\s{0,2}g(?!\w)', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "g",
        "gram",
        "grams",
    ]

