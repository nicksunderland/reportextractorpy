from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "weight",
                      "minor": "weight"}
    regex_rules = [
        re.compile(r'\b(?:(?i:weight?|wt[.:]?)|W(?:(?=\d|:)|(?=:?[ ]\d)))\b'),
    ]
    string_matches = [  # keep for testing regex
        "weight",
        "wt",
        "wt."
        "W 6stone"
    ]
