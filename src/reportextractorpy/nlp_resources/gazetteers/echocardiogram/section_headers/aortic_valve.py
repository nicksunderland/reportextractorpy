from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re

class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "aortic_valve"}
    regex_rules = [
        re.compile(r'(?:A(?:ortic|ORTIC) V(?:alve|ALVE))[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "Aortic Valve",
        "AORTIC VALVE",
        "Aortic Valve:",
    ]



