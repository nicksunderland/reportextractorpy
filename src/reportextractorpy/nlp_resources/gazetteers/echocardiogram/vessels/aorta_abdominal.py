from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "abdominal_aorta"}
    regex_rules = [
        re.compile(r'(?i)\babdo\.?(?:minal)?[ -]ao(?:rta)?\.?\b'),
    ]
    string_matches = [
        "abdominal aorta",
        "abdominal ao",
        "abdominal ao.",
    ]


