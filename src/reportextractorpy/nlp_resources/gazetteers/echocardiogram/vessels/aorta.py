from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "aorta"}
    regex_rules = [
        re.compile(r'\baorta\b', flags=re.I),
    ]
