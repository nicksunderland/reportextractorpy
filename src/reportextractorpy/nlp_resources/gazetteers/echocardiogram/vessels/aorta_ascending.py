from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "ascending_aorta"}
    regex_rules = [
        re.compile(r'(?i)\b(?:prox[.]?(?:imal)?[\s-]{0,2})?asc[.]?(?:ending)?[\s-]{0,2}ao[.]?(?:rta)?(?![a-z])'),
        re.compile(r'(?i)\bao[.]?(?:rta)?[\s-]{0,2}asc[.]?(?:ending)?(?![a-z])')
    ]
    string_matches = [  # keep for testing regex
        "proximal ascending aorta",
        "ascending aorta",
        "asc aorta",
        "asc. aorta",
        "proximal ascending ao",
        "prox ascending ao",
        "prox. ascending ao",
        "prox. asc. aorta",
        "prox. asc. ao.",
        "ascending aorta",
        "ascending ao",
        "ascending ao.",
        "asc ao",
        "asc ao.",
        "asc. ao.",
        "ao asc",
        "ao. asc",
        "ao. asc.",
        "ao asc."
    ]