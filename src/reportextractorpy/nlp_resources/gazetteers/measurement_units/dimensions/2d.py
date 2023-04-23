from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "dimension",
                      "minor": "2d"}
    regex_rules = [
        re.compile(r'\b(?<!\d)2\s?[-]?\s?d(?:imensions?(?:al)?)?\b', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "2d",
        "2D",
        "2-D",
        "2-d",
        "2 dimension",
        "2 dimensions",
        "2 dimensional",
        "2-dimensional"
    ]
