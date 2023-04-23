from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "speed",
                      "minor": "cm/sec"}
    regex_rules = [
        re.compile(r'(?:centimet[re]{2}s?|cms?)\s{0,2}'
                   r'(?:per|\/)\s{0,2}'
                   r'(?:sec(?:ond)?|s\b)', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "m / s",
        "m / s",
        "m / sec",
        "m / sec"
    ]



