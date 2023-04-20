from reportextractorpy.abstract_gazetteer import AbstractGazetteer


class Gazetteer(AbstractGazetteer):
    annot_type = "Units"
    annot_features = {"major": "length",
                      "minor": "cm"}
    string_matches = [  # input these as all lowercase
        "cm",
        "cms",
        "centimeter",
        "centimeters",
        "centimetre",
        "centimetres"
    ]
    regex_rules = r"""
    
    """.format(token_type=annot_type)
