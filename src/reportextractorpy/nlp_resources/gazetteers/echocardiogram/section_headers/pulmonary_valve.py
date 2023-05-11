from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "pulmonary_valve"}
    regex_rules = [
        re.compile(r'P(?:ULMONARY|ulmonary) V(?:ALVE|alve)?[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "Pulmonary Valve",
        "Pulmonary Valve:",
        "PULMONARY VALVE"
    ]
