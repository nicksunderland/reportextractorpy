from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "coronary_sinus"}
    regex_rules = [
        re.compile(r'(?i)\bcoronary sinus\b'),
    ]
