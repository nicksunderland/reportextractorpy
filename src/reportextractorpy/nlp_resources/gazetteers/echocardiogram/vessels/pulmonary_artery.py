from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "pulmonary_artery"}
    regex_rules = [
        re.compile(r'\b(?:(?i:pulmonary artery)|PA)\b'),
    ]
    string_matches = [
        "pulmonary artery",
        "PA"
    ]
