from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "image_quality"}
    regex_rules = [
        re.compile(r'(?:I(?:mage|MAGE)|Technical) Q(?:uality|UALITY)[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "IMAGE QUALITY",
        "IMAGE QUALITY:",
        "Technical Quality:"
    ]
