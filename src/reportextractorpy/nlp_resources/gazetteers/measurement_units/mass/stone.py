from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "mass",
                      "minor": "stone"}
    regex_rules = [
        re.compile(r'stones?|(?<=\d)(?:\s{0,2})st\.?(?![\w])', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "stone",
        "stones",
        "st",
        "st.",
    ]
