from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "cardiac_rhythm",
                      "minor": "sinus_rhythm"}
    regex_rules = [
        re.compile(r'\bSR\b'),
        re.compile(r'(?i)\bsinus rhyth?m\b'),
    ]
    string_matches = [
        "sinus rhythm",
        "sinus Rhythm",
        "Sinus Rhythm",
        "Sinus rhythm",
        "SINUS RHYTHM",
        "SR",
        "Sinus rhytm",
        "sinus rhytm"
    ]
