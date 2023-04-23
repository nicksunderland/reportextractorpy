from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length/length",
                      "minor": "mm/m"}
    regex_rules = [
        re.compile(r'(?:millimet[re]{2}s?|mms?)\s{0,2}'
                   r'(?:per|\/)\s{0,2}'
                   r'(?:met[re]{2}|m)', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "mm / m",
        "mm / m",
        "mm / m",
        "mm / m",
        "mms / m",
        "mm / m",
        "mm / m",
        "mm / m",
        "millimeter per meter",
        "millimeter/meter",
        "millimeters per meter",
        "millimeters/meter",
        "millimetre per metre",
        "millimetre/metre",
        "millimetres per meter",
        "millimetres/meter"
    ]



