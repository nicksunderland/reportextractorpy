from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "left_atrium"}
    regex_rules = [
        re.compile(r'(?:L(?:eft|EFT) A(?:trium|TRIUM)|CHAMB_LA_TEXT)[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "Left Atrium",
        "LEFT ATRIUM",
        "CHAMB_LA_TEXT"
    ]



