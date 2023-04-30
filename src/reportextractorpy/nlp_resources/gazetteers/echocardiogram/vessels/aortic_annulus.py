from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "aortic_annulus"}
    regex_rules = [
        re.compile(r'(?i)\bao[.]?(?:rt(?:a|ic))?[ ]annulus\b'),
        re.compile(r'\bA1(?:[ ][(]?annulus[)]?)?(?=[^\d])'),
        re.compile(r'MM_AORTIC_ANNULUS'),
    ]
    string_matches = [
        "aortic annulus"
        "aorta annulus",
        "A1 (annulus)"
        "A1"
    ]



