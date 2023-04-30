from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "quantity_change",
                      "minor": "increase"}
    regex_rules = [
        re.compile(r'(?i)\b(?:incre(?:ased?|ment(?:ed)?)|gain(?:ed)?|put(?:ting)?(?:\son)?)\b'),
    ]
    string_matches = [  # keep for testing regex
        "increased",
        "incremented",
        "gain",
        "gained",
        "put on",
        "putting on",
        "put",
    ]


