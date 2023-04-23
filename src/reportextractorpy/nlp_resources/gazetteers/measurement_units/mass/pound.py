from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "mass",
                      "minor": "pounds"}
    regex_rules = [
        re.compile(r'pounds?|(?<=\d)\s{0,2}lbs?(?!\w)', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "pound",
        "pounds",
        "lb",
        "lb.",
        "lbs.",
        "lbs"
    ]