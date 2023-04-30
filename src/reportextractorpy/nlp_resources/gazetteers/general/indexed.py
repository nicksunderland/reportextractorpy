from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "indexed",
                      "minor": "indexed"}
    regex_rules = [
        re.compile(r'(?i)\b(?:indexed|normali[sz]ed?|corrected)\b'),
    ]
    string_matches = [  # keep for testing regex
        "indexed",
        "normalised",
        "normalized",
        "corrected"
    ]
