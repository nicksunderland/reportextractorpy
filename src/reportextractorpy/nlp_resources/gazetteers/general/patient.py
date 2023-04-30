from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "patient",
                      "minor": "patient"}
    regex_rules = [
        re.compile(r'(?i)\bp(?:atien)?t(?:s|\'s|\.)?\b'),
    ]
    string_matches = [  # keep for testing regex
        "patient",
        "patients",
        "patient's",
        "Pt",
        "pt",
        "Pt.",
    ]
