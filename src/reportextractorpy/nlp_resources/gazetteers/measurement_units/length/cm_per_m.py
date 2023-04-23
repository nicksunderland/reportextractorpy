from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import re


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length/length",
                      "minor": "cm/m"}
    regex_rules = [
        re.compile(r'(?:centimet[re]{2}s?|cms?)\s{0,2}'
                   r'(?:per|\/)\s{0,2}'
                   r'(?:met[re]{2}|m)', flags=re.I)
    ]
    string_matches = [  # keep for testing regex
        "cm/m",
        "cm / m",
        "cm /m",
        "cm/ m",
        "cms/m",
        "cm per m",
        "cms per m",
        "centimeter per meter",
        "centimeter/meter",
        "centimeters per meter",
        "centimeters/meter",
        "centimetre per metre",
        "centimetre/metre",
        "centimetres per meter",
        "centimetres/meter"
    ]



