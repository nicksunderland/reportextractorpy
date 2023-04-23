from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "z_score",
                      "minor": "z1"}
    regex_rules = [
        re.compile(r'\bz1\b', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "z1",
    ]
