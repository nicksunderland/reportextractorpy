from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "right_sided_structures"}
    regex_rules = [
        re.compile(r'RIGHT (?:SIDED STRUCTURES|HEART)')
    ]
    string_matches = [  # keep for testing regex
        "RIGHT SIDED STRUCTURES",
        "RIGHT HEART",
    ]




