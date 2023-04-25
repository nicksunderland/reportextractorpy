from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator, GetNumberFromText, GetNumberFromNumeric, RemAnn
from gatenlp.pam.pampac import Rule, pampac_parsers
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self, mode: str):
        self.annotator_outset_name = ""
        self.var_name = ""
        self.included_annots = [("", "Numeric")]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        super().__init__(**self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        # numeric ranges rule
        pattern_2 = Seq(AnnAt(type="Numeric", name="value_1"),
                        Text(text=re.compile('(?:[-]|to[-]?)(?:\s[a]\s)?(?:max|min(?:imum)?)?(?:\sof)?', flags=re.I)),
                        AnnAt(type="Numeric", name="value_2"))
        action_2 = AddAnn(type="Numeric", features={"value": GetNumberFromText(name_1="value_1", name_2="value_2"),
                                                    "kind": "numeric_range"})

        # fractions rule
        pattern_1 = Seq(AnnAt(type="Numeric", name="value_1"),
                        Text(text=re.compile(r'/')),
                        AnnAt(type="Numeric", name="value_2"))
        action_1 = AddAnn(type="Numeric", features={"value": GetNumberFromNumeric(name_1="value_1",
                                                                                  name_2="value_2",
                                                                                  func=lambda x, y: float(x)/float(y)),
                                                    "kind": "fraction"})

        # orthogonal number rule
        pattern_3 = Seq(AnnAt(type="Numeric", name="value_1"),
                        Text(text=re.compile(r'\s?(?:x|by)\s?')),
                        AnnAt(type="Numeric", name="value_2"))
        action_3 = AddAnn(type="Numeric", features={"value_1": GetNumberFromNumeric(name_1="value_1"),
                                                    "value_2": GetNumberFromNumeric(name_2="value_2"),
                                                    "kind": "orthogonal_numbers"})

        # numeric categories / type description e.g. type 2 MI
        pattern_4 = Seq(Text(text=re.compile(r'type\s?', re.I)),
                        AnnAt(type="Numeric", name="value"))
        action_4 = AddAnn(type="Lookup", features={"value": GetNumberFromNumeric(name_1="value"),
                                                   "kind": "numeric_category"})

        return [Rule(pattern_2, action_2),
                Rule(pattern_1, action_1),
                Rule(pattern_3, action_3),
                Rule(pattern_4, action_4)]
