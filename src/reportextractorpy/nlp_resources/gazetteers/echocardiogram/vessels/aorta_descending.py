from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "descending_aorta"}
    regex_rules = [
        re.compile(r'(?i)\bdesc\.?(?:ending)?[ -](?:limb of (?:the )?)?ao(?:rt(?:a|ic))?\b'),
        re.compile(r'CHAMB_AO_DESC_TEXT|CHAMB_AO_DESC_NORMAL|MM_DESCENDING_AORTA'),
    ]
