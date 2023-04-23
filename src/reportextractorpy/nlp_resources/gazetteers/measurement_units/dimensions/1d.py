from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "dimension",
                      "minor": "1d"}
    regex_rules = [
        re.compile(r'\b(?<!\d)1\s?[-]?\s?d(?:imension(?:al)?)?\b', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "1d",
        "1D",
        "1-D",
        "1-d",
        "1 dimension",
        "1 dimensional",
        "1-dimensional"
    ]
