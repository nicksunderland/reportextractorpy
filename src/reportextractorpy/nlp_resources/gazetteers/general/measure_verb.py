from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "measure_verb",
                      "minor": "measure_verb"}
    regex_rules = [
        re.compile(r'(?i)\bmeasur(?:ing|e[sd]?)\b'),
    ]
    string_matches = [  # keep for testing regex
        "measure",
        "measured",
        "measuring",
        "measures"
    ]