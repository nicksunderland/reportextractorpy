from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length/area",
                      "minor": "mm/m2"}
    regex_rules = [
        re.compile(r'(?:millimet[re]{2}s?|mms?)\s{0,2}'
                   r'(?:per|\/)\s{0,2}'
                   r'(?:m(?:et[re]{2}s)?)\s{0,2}'
                   r'(?:squared|sq|[s2\u00B2_]?)', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "mm / msq",
        "mm / m2",
        "mm / m_",
        "mm / m²",
    ]
    


