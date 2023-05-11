from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "right_ventricle"}
    regex_rules = [
        re.compile(r'(?:The |THE )?R(?:IGHT|ight) V(?:entricle|ENTRICLE)')
    ]
    string_matches = [  # keep for testing regex
        "Right Ventricle",
        "RIGHT VENTRICLE",
        "Right Ventricle:",
        "The Right Ventricle"
    ]



