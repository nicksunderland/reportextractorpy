from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "cardiac_rhythm",
                      "minor": "heart_rate"}
    regex_rules = [
        re.compile(r'\bHR|[Hh]eart [Rr]ate|HEART RATE|Ht [rR]ate\b'),
    ]
    string_matches = [
        "heart rate",
        "HEART RATE",
        "HR",
        "Ht rate",
        "Ht Rate",
    ]





