from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "measurements"}
    regex_rules = [
        re.compile(r'Measurements:')
    ]
    string_matches = [  # keep for testing regex
        "Measurements:",
    ]

