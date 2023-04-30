from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "grammar",
                      "minor": "preposition"}
    regex_rules = [
        re.compile(r'(?i)\b(?:(?:away\s)?from|with|to|on|of|at)\b'),
    ]
    string_matches = [  # keep for testing regex
        "at",
        "TO",
        "on",
        "from"
        "away from",
        "of",
        "with"
    ]
