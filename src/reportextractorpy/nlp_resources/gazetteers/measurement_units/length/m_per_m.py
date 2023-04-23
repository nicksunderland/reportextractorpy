from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length/length",
                      "minor": "m/m"}
    regex_rules = [
        re.compile(r'(?:met[re]{2}s?|ms?)\s{0,2}'
                   r'(?:per|\/)\s{0,2}'
                   r'(?:met[re]{2}|m)', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "m/m"
    ]



