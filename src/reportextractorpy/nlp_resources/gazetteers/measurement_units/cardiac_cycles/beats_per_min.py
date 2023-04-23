from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "cardiac_cycles",
                      "minor": "bpm"}
    regex_rules = [
        re.compile(r'beats?\s{0,2}(?:per|\/)\s{0,2}min(?:ute)?|'
                   r'(?:(?<=\d)|(?<=\b))bpm\b', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "beats per minute",
        "BEATS / MINUTE",
        "bpm",
        "BPM",
    ]
