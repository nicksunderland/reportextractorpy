from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from gatenlp.pam.pampac import Rule, pampac_parsers
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self, mode: str):
        super().__init__(
            annotator_outset_name=mode,
            rule_list=self.gen_rule_list(),
            var_name="ao_sov",
            included_annots=[("", ["Token", "Anatomy", "Units"])],
            pampac_skip="longest",
            pampac_select="first")

    def gen_rule_list(self) -> List[Rule]:
        rules = self.context_v1_unit_rules() + \
                self.context_v1v2_unit_rules()
        return rules

    def context_v1_unit_rules(self) -> List[Rule]:
        patterns = [
            Seq(AnnAt(type="Anatomy", name="context"),
                AnnAt(type="Token", name="value"),
                AnnAt(type="Units", name="units"))
        ]
        return [Rule(pat, self.action_v1v2unit_match) for pat in patterns]

    def context_v1v2_unit_rules(self) -> List[Rule]:
        patterns = [
            Seq(AnnAt(type="Anatomy", name="context"),
                AnnAt(type="Token", features=dict(kind="number"), name="value_1"),
                N(Text(text=re.compile(r'-(?:to-)?')), min=0, max=1),
                AnnAt(type="Token", features=dict(kind="number"), name="value_2"),
                AnnAt(type="Units", name="units"))
        ]
        return [Rule(pat, self.action_v1v2unit_match) for pat in patterns]