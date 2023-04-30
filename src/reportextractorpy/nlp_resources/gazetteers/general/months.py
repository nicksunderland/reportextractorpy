from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "month",
                      "minor": "month"}
    regex_rules = [
        re.compile(r'(?i)\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|(?:Nov|Dec)(?:ember)?)\b'),
    ]
    string_matches = [  # keep for testing regex
        "January"
    ]