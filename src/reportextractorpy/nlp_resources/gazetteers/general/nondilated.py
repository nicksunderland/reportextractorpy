from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Categorical"
    annot_features = {"major": "size_category",
                      "minor": "nondilated"}
    regex_rules = [
        re.compile(r'(?i)\b(?:non-?(?:dilat(?:ed|(?:at)?ion)|enlarged)|normal)\b'),
    ]
    string_matches = [  # keep for testing regex
        "nondilated",
        "non-dilated",
        "nonenlarged",
        "non-enlarged",
        "normal",
    ]