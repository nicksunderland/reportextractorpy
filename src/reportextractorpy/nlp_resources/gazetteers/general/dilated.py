from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Categorical"
    annot_features = {"major": "size_category",
                      "minor": "dilated"}
    regex_rules = [
        re.compile(r'(?i)\b(?:(?<!non-)dilat(?:ed|(?:at)?ion)|enlarged|increased\s(?:in\s)?size)\b'),
    ]
    string_matches = [  # keep for testing regex
        "dilated",
        "enlarged",
        "dilation",
        "dilatation",
        "increased size",
        "increased in size"
    ]