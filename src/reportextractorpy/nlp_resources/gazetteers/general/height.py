from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "height",
                      "minor": "height"}
    regex_rules = [
        re.compile(r'\b(?:(?i:height?|ht[.:]?)|H(?:(?=\d|:)|(?=:?[ ]\d)))\b'),
    ]
    string_matches = [  # keep for testing regex
        "weight",
        "wt",
        "wt."
        "W"
    ]
    