from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "mass",
                      "minor": "kg"}
    regex_rules = [
        re.compile(r'kilograms?|(?<=\d)\s{0,2}kgs?(?!\w)', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "kg",
        "kgs",
        "kilogram",
        "kilograms",
    ]

