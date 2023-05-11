from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "left_ventricle"}
    regex_rules = [
        re.compile(r'(?:The )?(?:(?<=The )l|L)(?:(?:eft|EFT|V) (?:V(?:entricle|ENTRICLE)|MEASUREMENTS)|CHAMB_LA_TEXT)[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "LEFT VENTRICLE",
        "LEFT VENTRICLE:",
        "Left Ventricle:",
        "LV MEASUREMENTS",
        "The left Ventricle",
        "The Left Ventricle"
    ]







