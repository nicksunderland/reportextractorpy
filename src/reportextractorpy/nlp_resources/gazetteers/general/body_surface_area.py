from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "body_surface_area",
                      "minor": "body_surface_area"}
    regex_rules = [
        re.compile(r'(?i)\b(?:bsa|body surface area)\b'),
    ]
    string_matches = [  # keep for testing regex
        "body surface area",
        "BSA",
    ]