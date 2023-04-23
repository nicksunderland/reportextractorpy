from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "volume/time",
                      "minor": "ml/hr"}
    regex_rules = [
        re.compile(r'(?<![a-z])(?:m(?:illilit[re]{2})?s?|mls?)\s{0,2}'
                   r'(?:per|\/)\s{0,2}'
                   r'(?:h(?:ou)?r?)', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "ml/hr",
        "ml / hr",
        "ml/hour"
    ]



