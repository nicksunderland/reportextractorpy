from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "SectionHeader"
    annot_features = {"major": "header",
                      "minor": "summary"}
    regex_rules = [
        re.compile(r'(?:(?:S(?:UMMARY|ummary))|(?:C(?:ONCLUSION|onclusion))|OVERALL_IMPRESSION)[ :-]{0,2}')
    ]
    string_matches = [  # keep for testing regex
        "SUMMARY",
        "Summary",
        "Summary:",
        "OVERALL_IMPRESSION:",
        "Conclusion",
        "CONCLUSION"
    ]
