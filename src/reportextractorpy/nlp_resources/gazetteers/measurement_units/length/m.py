from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length",
                      "minor": "m"}
    regex_rules = [
        re.compile(r'(?:(?<=\d)|(?<=\b))ms?\b', flags=re.I),
        re.compile(r'met[re]{2}s?', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "m",
        "ms",
        "meter",
        "meters",
        "metre",
        "metres",
    ]
