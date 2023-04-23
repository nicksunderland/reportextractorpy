from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length",
                      "minor": "cm"}
    regex_rules = [
        re.compile(r'(?:(?<=\d)|(?<=\b))cms?\b', flags=re.I),
        re.compile(r'centimet[re]{2}s?', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "cm",
        "cms",
        "centimeter",
        "centimeters",
        "centimetre",
        "centimetres"
    ]

