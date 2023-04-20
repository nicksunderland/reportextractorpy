from reportextractorpy.abstract_gazetteer import AbstractGazetteer


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "aorta"}
    string_matches = [
        "aorta"
    ]
    regex_rules = r"""
    
        """.format(annot_type=annot_type)
