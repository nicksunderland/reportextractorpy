from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "pressure",
                      "minor": "mmhg"}
    regex_rules = [
        re.compile(r'mmhg', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "mmhg",
    ]
