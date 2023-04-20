from reportextractorpy.abstract_gazetteer import AbstractGazetteer


class Gazetteer(AbstractGazetteer):
    annot_type = "Anatomy"
    annot_features = {"major": "aorta",
                      "minor": "sinotubular_junction"}
    string_matches = [  # input these as all lowercase
        "stj",
        "s.t.j",
        "st junction",
        "st junc",
        "sino tube junction",
        "sinotube junction",
        "sinotubular junction",
        "sino-tubular junction",
        "sino tubular junction",
        "sinuo tubular junction",
        "sinuotubular junction",
        "mm_sinotubular_junction",
        "sinotub",
        "sinotube",
    ]
    regex_rules = r"""
    
    """.format(annot_type=annot_type)
