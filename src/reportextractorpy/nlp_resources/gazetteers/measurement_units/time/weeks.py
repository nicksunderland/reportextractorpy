from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "time",
                      "minor": "weeks"}
    regex_rules = [
        re.compile(r'(?<![a-z])weeks?\b', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "weeks",
    ]
