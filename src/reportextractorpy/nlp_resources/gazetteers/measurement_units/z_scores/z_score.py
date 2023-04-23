from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "z_score",
                      "minor": "z_score"}
    regex_rules = [
        re.compile(r'(?<![a-z])z\s{0,2}[-_=]?\s{0,2}(?:score)?', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "z-score",
        "z score",
        "z_score",
        "Z=",
        "Z =",
    ]
