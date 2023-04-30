from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "aortic_root"}
    regex_rules = [
        re.compile(r'(?i)\bprox(?:[.]|imal)?[ ]ao(?:rta)?[.]?\b'),
        re.compile(r'(?i)\bao(?:[.]|[rti]{3}c|rta)?(?:[ ]root)?\b'),
        re.compile(r'MM_AO_ROOT|HAMB_AO_ASC_TEXT|HAMB_AO_ASC_NORMAL'),
    ]
    string_matches = [
        "aortic root",
        "aorta root",
        "AORITC ROOT",
        "MM_AO_ROOT",
        "ao.",
        "Ao. Root",
        "AO root",
        "proximal aorta",
        "prox. aorta",
        "HAMB_AO_ASC_TEXT",
        "HAMB_AO_ASC_NORMAL"
    ]


