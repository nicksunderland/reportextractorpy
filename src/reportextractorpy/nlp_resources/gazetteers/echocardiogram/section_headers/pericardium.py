from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "pericardium"}
    regex_rules = [
        re.compile(r'PERICARDIUM[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "PERICARDIUM:"
    ]



