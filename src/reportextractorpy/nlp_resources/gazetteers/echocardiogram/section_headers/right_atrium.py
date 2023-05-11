from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "right_atrium"}
    regex_rules = [
        re.compile(r'R(?:ight|IGHT) [Aa](?:TRIUM|trium)?[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "RIGHT ATRIUM",
        "Right Atrium",
        "Right atrium:"
    ]




