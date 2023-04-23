from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "dimension",
                      "minor": "3d"}
    regex_rules = [
        re.compile(r'\b(?<!\d)3\s?[-]?\s?d(?:imensions?(?:al)?)?\b', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "3d",
        "3D",
        "3-D",
        "3-d",
        "3 dimension",
        "3 dimensions",
        "3 dimensional",
        "3-dimensional"
    ]
