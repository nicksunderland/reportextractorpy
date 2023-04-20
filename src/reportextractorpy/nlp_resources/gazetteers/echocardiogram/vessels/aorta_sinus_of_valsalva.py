from reportextractorpy.abstract_gazetteer import AbstractGazetteer


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "sinus_of_valsalva"}
    string_matches = [  # input these as all lowercase
        "sov",
        "s.o.v",
        "sinus of valsalva",
        "sinus valsalva",
        "sinus fo valsalva",
        "sinus of valslava",
        "mm_sinus_of_valsalva",
        "sinoval"
    ]
    regex_rules = r"""

    
    """.format(annot_type=annot_type)
