from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length",
                      "minor": "feet"}
    regex_rules = [
        re.compile(r'f(?:oo|ee)t|(?:(?<=\d)|(?<=\b))ft\.?|(?<=\d)\s?[\'`]', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "foot",
        "feet",
        "ft",
        "ft.",
        "'",
        "`"
    ]




