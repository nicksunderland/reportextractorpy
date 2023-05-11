from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "normal_study"}
    regex_rules = [
        re.compile(r'NORMAL_STUDY')
    ]
    string_matches = [  # keep for testing regex
        "NORMAL_STUDY"
    ]

