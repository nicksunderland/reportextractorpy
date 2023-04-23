from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "time",
                      "minor": "msec"}
    regex_rules = [
        re.compile(r'(?<![a-z])m(?:illi)?s(?:ec)?(?:ond)?s?', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "ms",
        "msec",
        "millisec",
        "millisecond"
    ]
