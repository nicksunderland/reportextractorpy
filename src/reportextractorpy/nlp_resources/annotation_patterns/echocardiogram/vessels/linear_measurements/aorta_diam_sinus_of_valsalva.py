from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List


class Pattern(AbstractPatternAnnotator):

    def __init__(self, mode: str):
        self.init_vars = {
            "annotator_outset_name": mode,
            "rules": None,
            "var_name": "ao_sov",
            "included_annots": [("", ["Token", "Anatomy"])],
            "pampac_skip": "longest",
            "pampac_select": "first"
        }
        self.init_vars.update({"rules": self.gen_rule_list()})
        super().__init__(**self.init_vars)

    def gen_rule_list(self) -> List[Rule]:
        #"""Text: this sov 3 cm"""
        pat1 = Seq(AnnAt(type="Anatomy", name="context"),
                   AnnAt(type="Token", name="value"),
                   AnnAt(type="Token", name="units"), name=self.init_vars["var_name"])

        rule1 = Rule(pat1, self.action_v1v2unit_match, priority=0)

        return [rule1]
