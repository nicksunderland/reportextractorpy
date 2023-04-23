from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "speed",
                      "minor": "m/sec"}
    regex_rules = [
        re.compile(r'(?<![a-z])(?:met[re]{2}s?|ms?)\s{0,2}'
                   r'(?:per|\/)\s{0,2}'
                   r'(?:sec(?:ond)?s?|s\b)', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "m / s",
        "m / s",
        "m / sec",
        "m / sec"
    ]



