from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "mitral_valve"}
    regex_rules = [
        re.compile(r'M(?:ITRAL|itral) V(?:ALVE|alve)?[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "MITRAL VALVE",
        "Mitral Valve",
        "Mitral Valve:",
    ]
