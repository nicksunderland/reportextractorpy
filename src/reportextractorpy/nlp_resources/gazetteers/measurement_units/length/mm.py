from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length",
                      "minor": "mm"}
    regex_rules = [
        re.compile(r'(?:(?<=\d)|(?<=\b))mms?\b', flags=re.I),
        re.compile(r'millimet[re]{2}s?', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "mm",
        "mms",
        "millimeter",
        "millimeters",
        "millimetre",
        "millimetres",
    ]
