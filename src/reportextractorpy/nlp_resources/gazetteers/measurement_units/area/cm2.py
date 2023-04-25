from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "area",
                      "minor": "cm2"}
    regex_rules = [
        re.compile(r'(?:centimet[re]{2}s?|cm)\s{0,2}(?:(?:squared|sqr?d?)|[2_^\u00B2]{1,2})', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "cm2",
        "cm sq",
        "cm sq."
        "cm^2",
        "cm_",
        "cmsq",
        "cm²"
    ]
