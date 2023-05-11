from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "miscellaneous"}
    regex_rules = [
        re.compile(r'M(?:ISC|isc)(?:ELLANEOUS|ellaneous)?[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "MISC",
        "MISCELLANEOUS",
        "Misc",
        "Miscellaneous",
        "Miscellaneous:"

    ]
