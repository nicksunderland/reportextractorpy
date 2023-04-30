from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "quantity_change",
                      "minor": "decrease"}
    regex_rules = [
        re.compile(r'(?i)\b(?:decre(?:ased?|ment(?:ed)?)|lost)\b'),
    ]
    string_matches = [  # keep for testing regex
        "decreased",
        "decrease",
        "decremented",
        "lost",
    ]


