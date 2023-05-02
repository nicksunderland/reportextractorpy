from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Seq, Text, N, Lookahead, Ann, Or
from gatenlp.pam.matcher import IfNot, FeatureMatcher, AnnMatcher, isIn, FeatureEqMatcher
from gatenlp.pam.pampac import AddAnn
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self):
        self.var_name = ""
        self.outset_name = ""
        self.included_annots = [("", ["Numeric", "Token", "Units"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []

        """
        Feet +/- inches
        Description: measurements in feet and inches (allowing a token inbetween, e.g. comma or fullstop)
        optional inches units
        Example: '6 feet 5 inches'
        """
        pattern_1 = Seq(
                        # Numeric annotation
                        AnnAt(type="Numeric", name="value_1"),
                        # Units annotation
                        AnnAt(type="Units", features=FeatureMatcher(minor="feet")),
                        # Optional sequence of joining phrase (optional) & numeric, followed by an optional inches
                        # unit (lookahead to check units aren't related to mass first before capturing)
                        Seq(Lookahead(parser=Seq(AnnAt(text=re.compile('(?i)[&,.]|and')).repeat(0, 1),
                                                 AnnAt(type="Numeric", name="value_2")),
                                      laparser=AnnAt().notoverlapping(type="Units", features=FeatureMatcher(major="mass"))),
                            AnnAt(type="Units", features=FeatureMatcher(minor="inches")).repeat(0, 1)).repeat(0, 1))

        action_1 = AddAnn(type="ImperialMeasurement", features={"major": "length",
                                                                "feet": GetNumberFromNumeric(name_1="value_1"),
                                                                "inches": GetNumberFromNumeric(name_2="value_2", silent_fail=True)})
        rule_list.append(Rule(pattern_1, action_1))

        """
        Feet units not present
        Description: measurements in feet and inches, but where the feet unit is implied
        Example: '6 5inches'
        """
        # measurements in feet and inches (allowing a token inbetween, e.g. comma or fullstop)
        # optional feet units
        pattern_2 = Seq(AnnAt(type="Numeric", name="value_1"),
                        AnnAt(type="Units", features=FeatureMatcher(minor="feet")).repeat(0, 1),
                        AnnAt(type="Numeric", name="value_2"),
                        AnnAt(type="Units", features=FeatureMatcher(minor="inches")))

        action_2 = AddAnn(type="ImperialMeasurement", features={"major": "length",
                                                                "feet": GetNumberFromNumeric(name_1="value_1", silent_fail=True),
                                                                "inches": GetNumberFromNumeric(name_2="value_2")})
        rule_list.append(Rule(pattern_2, action_2))

        """
        Inches only
        Description: measurements inches only
        Example: '52 inches'
        """
        pattern_3 = Seq(AnnAt(type="Numeric", name="value_2"),
                        AnnAt(type="Units", features=FeatureMatcher(minor="inches")))
        action_3 = AddAnn(type="ImperialMeasurement", features={"major": "length",
                                                                "feet": GetNumberFromNumeric(name_1="value_1", silent_fail=True),
                                                                "inches": GetNumberFromNumeric(name_2="value_2")})
        rule_list.append(Rule(pattern_3, action_3))

        return rule_list
