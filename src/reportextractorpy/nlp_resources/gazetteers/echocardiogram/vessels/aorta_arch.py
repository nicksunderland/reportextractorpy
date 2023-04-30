from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "aortic_arch"}
    regex_rules = [
        re.compile(r'(?i)\bao(?:rt(?:a|ic))?[ -]arch\b'),
        re.compile(r'CHAMB_AO_ARCH_TEXT|HAMB_AO_ARCH_NORMAL'),
    ]