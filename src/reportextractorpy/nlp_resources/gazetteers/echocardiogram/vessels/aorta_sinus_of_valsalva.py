from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re

class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "sinus_of_valsalva"}
    regex_rules = [
        re.compile(r'\bsinus[\s-]{0,2}(?:[of]{2})?[\s-]{0,2}vals[alv]{4}\b', flags=re.I),
        re.compile(r'mm_sinus_of_valsalva', flags=re.I),
        re.compile(r'\bs[.\s]?o[.\s]?v[.\s]?\b', flags=re.I),
        re.compile(r'sinoval', flags=re.I)
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

