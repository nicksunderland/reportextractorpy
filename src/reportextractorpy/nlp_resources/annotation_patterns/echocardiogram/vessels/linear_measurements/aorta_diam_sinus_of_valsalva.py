from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator, GetNumberFromNumeric, \
    GetNumberFromText, RemAnn
from gatenlp.pam.pampac import Rule, pampac_parsers
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self, mode: str):
        self.annotator_outset_name = mode
        self.var_name = "ao_sov"
        self.included_annots = [("", ["Token", "Anatomy", "Numeric", "Units"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        super().__init__(**self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        pattern_1 = Seq(AnnAt(type="Anatomy", features=dict(minor="sinus_of_valsalva"), name="context"),
                        AnnAt(type="Numeric", name="value"),
                        AnnAt(type="Units", name="units"))

        action_1 = AddAnn(type=self.var_name, features={"context": GetText(name="context"),
                                                        "value": GetNumberFromNumeric(name_1="value"),
                                                        "units": GetText(name="units")})

        pattern_2 = Seq(
            AnnAt(type="Anatomy", features=dict(minor="sinus_of_valsalva"), name="context"),
            AnnAt(type="Numeric", name="value_1"),
            N(Text(text=re.compile(r'-(?:to-)?')), min=0, max=1),
        #
        #     ({Token.string == ~ "(?i)[-]|(to)"})
        # # 		({SpaceToken}{Token.string ==~ "(?i)a"})?
        # # 			({SpaceToken}{Token.string ==~ "(?i)(max)|(min)"})?
        #
        #
            AnnAt(type="Numeric", name="value_2"),
            AnnAt(type="Units", name="units"), name=self.var_name)
        #
        action_2 = AddAnn(type=self.var_name, features={"context": GetText(name="context"),
                                                        "value": GetNumberFromNumeric(name_1="value_1", name_2="value_2"),
                                                        "units": GetText(name="units")})

        return [Rule(pattern_1, action_1),
                Rule(pattern_2, action_2)]
