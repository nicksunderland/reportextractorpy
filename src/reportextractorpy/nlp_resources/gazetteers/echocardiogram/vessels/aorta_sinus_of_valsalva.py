from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re

class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "sinus_of_valsalva"}
    regex_rules = [
        re.compile(r'(?i)\bsinus[\s-]{0,2}(?:[of]{2})?[\s-]{0,2}vals[alv]{4}\b'),
        re.compile(r'(?i)mm_sinus_of_valsalva'),
        re.compile(r'(?i)\bs[.\s]?o[.\s]?v[.\s]?\b'),
        re.compile(r'(?i)sinoval')
    ]
    string_matches = [  # keep for testing regex
        "sov",
        "s.o.v",
        "sinus of valsalva",
        "sinus valsalva",
        "sinus fo valsalva",
        "sinus of valslava",
        "mm_sinus_of_valsalva",
        "sinoval"
    ]

