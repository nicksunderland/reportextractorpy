from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re

class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "sinotubular_junction"}
    regex_rules = [
        re.compile(r'\bs(?:in[uo]{1,2})?[\s.-]?t(?:ube?(?:ular)?)?[\s.-]?j(?:unc(?:tion)?)?[\s.-]?\b', flags=re.I),
        re.compile(r'mm_sinotubular_junction', flags=re.I),
        re.compile(r'\bsinotube?\b', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "stj",
        "s.t.j",
        "st junction",
        "st junc",
        "sino tube junction",
        "sinotube junction",
        "sinotubular junction",
        "sino-tubular junction",
        "sino tubular junction",
        "sinuo tubular junction",
        "sinuotubular junction",
        "mm_sinotubular_junction",
        "sinotub",
        "sinotube",
    ]

