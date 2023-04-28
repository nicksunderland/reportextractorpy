from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented
        self.templates = [{"var_name": "ao_sov",      "descriptor": "sinus_of_valsalva"},
                          {"var_name": "ao_stj_diam", "descriptor": "sinotubular_junction"},
                          {"var_name": "ao_asc_diam", "descriptor": "ascending_aorta"}]
        self.outset_name = "echocardiogram"
        self.included_annots = [("", ["Token", "Anatomy", "Numeric", "Units"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:

        pattern_1 = Seq(AnnAt(type="Anatomy", features=dict(minor=self.descriptor), name="context"),
                        AnnAt(type="Numeric", name="value"),
                        AnnAt(type="Units", features=dict(major="length"), name="units"))

        action_1 = AddAnn(type=self.var_name, features={"context": GetText(name="context"),
                                                        "value": GetNumberFromNumeric(name_1="value"),
                                                        "units": GetText(name="units", silent_fail=True)})

        rule_list = [
            Rule(pattern_1, action_1)
        ]

        return rule_list
