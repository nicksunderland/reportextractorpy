from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "tricsupid_valve"}
    regex_rules = [
        re.compile(r'T(?:RICUSPID|ricuspid) V(?:ALVE|alve)?[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "TRICUSPID VALVE",
        "Tricuspid Valve",
        "Tricuspid Valve:",
    ]
