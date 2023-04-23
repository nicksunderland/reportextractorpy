from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length",
                      "minor": "inches"}
    regex_rules = [
        re.compile(r'inch(?:es)?|'
                   r'(?:(?<=\d)|(?<=\b))in(?![\w])\.?|'
                   r'(?<=\d)\s?(?:["]|[\'`]{2})', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "inch",
        "inches",
        "in.",
        "in",
        "\"",
        "``",
        "\'\'"
    ]
