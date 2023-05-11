from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase, FeatureMatcher
from typing import List
import re


class TagReportSections(AbstractPatternAnnotator):
    """
    Description:
    Tag whole sections of text as report sections, depending on the report headers
    listed in the gazetteer files
    """

    def __init__(self, outset_name):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented
        self.templates = [{"descriptor": "aorta"},
                          {"descriptor": "aortic_valve"},
                          {"descriptor": "left_ventricle"}]
        self.outset_name = ""
        self.included_annots = [("", ["Sentence", "SectionHeader"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []
        section_pat = (
                AnnAt(type="Sentence")
                .covering(type="SectionHeader", features=FeatureMatcher(type=self.descriptor)) >>

                AnnAt(type="Sentence")
                .notcovering(type="SectionHeader", features=IfNot(FeatureMatcher(type=self.descriptor)))
                .repeat(0, 20)
        )
        section_act = AddAnn(type="ReportSection", features={"type": self.descriptor})
        rule_list.append(Rule(section_pat, section_act))

        return rule_list
