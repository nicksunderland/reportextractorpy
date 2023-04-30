from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Lookup"
    annot_features = {"major": "approximate",
                      "minor": "approximate"}
    regex_rules = [
        re.compile(r'(?i)\bapprox\.?(?:imate(?:ly)?)?\b'),
    ]
    string_matches = [  # keep for testing regex
        "approx.",
        "approximate",
        "approximately"
    ]
