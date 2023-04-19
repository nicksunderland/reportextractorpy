annot_type = "Anatomy"
annot_features = {"major": "aorta",
                      "minor": "ascending_aorta"}
string_matches = [  # input these as all lowercase
        "proximal ascending aorta",
        "ascending aorta",
        "asc aorta",
        "asc. aorta",
        "proximal ascending ao",
        "prox ascending ao",
        "prox. ascending ao",
        "prox. asc. aorta",
        "prox. asc. ao.",
        "ascending aorta",
        "ascending ao",
        "ascending ao.",
        "asc ao",
        "asc ao.",
        "asc. ao.",
        "ao asc",
        "ao. asc",
        "ao. asc.",
        "ao asc."
    ]
regex_rules = r"""
    
    """.format(token_type=annot_type,
               major_feature=annot_features["major"],
               minor_feature=annot_features["minor"])
