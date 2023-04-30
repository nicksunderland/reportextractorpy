from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "grammar",
                      "minor": "demonstrative_determiner"}
    regex_rules = [
        re.compile(r'(?i)\bth(?:is|at|[eo]se)\b'),
    ]
    string_matches = [  # keep for testing regex
        "this",
        "That",
        "these",
        "Those",
    ]
