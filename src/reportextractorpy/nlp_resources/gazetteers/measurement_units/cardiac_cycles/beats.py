from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "cardiac_cycles",
                      "minor": "beats"}
    regex_rules = [
        re.compile(r'beats|complexes', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "beats",
        "BEATS",
        "Beats",
        "complexes",
    ]
