from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re

class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "aorta"}
    regex_rules = [
        re.compile(r'(?:Aorta|AORTA|AO|HAMB_AO_ASC_TEXT|[Gg]reat [vV]essels)[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "Aorta",
        "Aorta:",
        "AORTA",
        "AO -",
        "AO-",
        "AO:",
        "HAMB_AO_ASC_TEXT",
        "Great Vessels"
    ]
