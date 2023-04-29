from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "image_frame",
                      "minor": "image_frame"}
    regex_rules = [
        re.compile(r'\b(?:images?|frames?)\b', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "image",
        "images",
        "frame",
        "frames"
    ]