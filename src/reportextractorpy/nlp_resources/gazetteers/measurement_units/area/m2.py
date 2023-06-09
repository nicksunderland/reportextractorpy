from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "area",
                      "minor": "m2"}
    regex_rules = [
        re.compile(r'(?<!centi)(?:met[re]{2}s?|(?<![cm])m(?!m))\s{0,2}(?:(?:squared|sqr?d?)|[2_^\u00B2]{1,2})', flags=re.I),
    ]
    string_matches = [  # keep for testing regex
        "m2"
        "m sq",
        "m sq.",
        "m^2",
        "m_",
        "m²"
    ]
