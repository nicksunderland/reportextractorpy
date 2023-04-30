from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "aortic_graft"}
    regex_rules = [
        re.compile(r'(?i)\b(?:aort(?:a|ic)|root)[ -](?:graft|replacement)\b', flags=re.I),
    ]
    string_matches = [
        "aortic graft",
        "root replacement",
    ]
