from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Categorical"
    annot_features = {"major": "modifier",
                      "minor": "negative_modifier"}
    regex_rules = [
        re.compile(r'(?i)\b(?:(?:is|does)no?\'?t|no[nt]?|outside|(?:more|greater|less)\sthan|neither)\b'),
    ]
    string_matches = [  # keep for testing regex
        "not",
        "non",
        "isn't",
        "isnt",
        "doesn't",
        "doesnt"
        "isnot",
        "no",
        "outside",
        "more than",
        "greater than",
        "less than",
        "neither"
    ]

