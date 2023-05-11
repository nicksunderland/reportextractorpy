from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric, ParseNumericUnits
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Seq, Text, N, Lookahead, Ann, Or
from gatenlp.pam.matcher import IfNot, FeatureMatcher, AnnMatcher, isIn, FeatureEqMatcher
from gatenlp.pam.pampac import AddAnn, Rule, GetText, UpdateAnnFeatures, GetAnn
from typing import List
import re


class TagVarSentenceWeight(AbstractPatternAnnotator):
    def __init__(self, outset_name):
        self.var_name = "VarSentence"
        self.outset_name = ""
        self.included_annots = [("", ["Sentence", "Lookup", "Anatomy"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []
        """
        TagVarSentence
        Description: Tag sentences that contain a mention of weight, or simply 'patient',
        Example: 'weight is 150kg', 'the patient is 159kg'
        """
        ht_sent_pat = Or(AnnAt(type="Sentence")
                         .covering(type="Lookup", features=FeatureMatcher(minor="weight"))
                         .notcovering(type="Anatomy"),
                         AnnAt(type="Sentence")
                         .covering(type="Lookup", features=FeatureMatcher(minor="patient"))
                         .notcovering(type="Anatomy"))
        ht_sent_act = AddAnn(type="VarSentence", features={"type": "weight"})
        rule_list.append(Rule(ht_sent_pat, ht_sent_act))
        return rule_list


class PatientWeight(AbstractPatternAnnotator):
    def __init__(self, outset_name):
        self.var_name = "weight"
        self.outset_name = outset_name
        self.included_annots = [("", ["Token", "VarSentence", "Anatomy", "Numeric", "Units", "Lookup", "Split",
                                      "ImperialMeasurement", "ReportSection", "Measurement", "Categorical"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []
        """
        PatientWeight
        Description:
        Example: 'weight is 150kg', 'the patient is 159kg'
        """
        """
        Macro: CONTEXT
        """
        context = \
            AnnAt(type="Lookup", features=FeatureMatcher(minor="weight"), name="context")

        """
        Macro: FILTER
        """
        token_filter = \
            AnnAt(type="Token")\
            .notat(type="Lookup", features=FeatureMatcher(minor=re.compile(r"(?i)indexed|body_surface_area"))) \
            .notat(type="Lookup", features=FeatureMatcher(major=re.compile(r"(?i)quantity_change"))) \
            .notat(type="ReportSection")\
            .notat(type="Anatomy")\
            .notat(type="Measurement")

        """
        Macro: METRIC_WEIGHT
        """
        metric_weight = AnnAt(type="Numeric", name="value")

        """        
        Macro: IMPERIAL_WEIGHT
        """
        imperial_weight = \
            AnnAt(type="ImperialMeasurement", features=FeatureMatcher(major="mass"), name="value")

        """
        Macro: METRIC_WEIGHT_UNITS
        """
        metric_weight_units = \
            AnnAt(type="Units", features=FeatureMatcher(major="mass"), name="units")

        """
        Blocker 1
        Description: Block things such as:
        Examples: 'patient reports 20kg weight loss'
        """
        blocker_1 = (
            (context |
             AnnAt(type="Lookup", features=FeatureMatcher(minor="patient"))
             .within(type="VarSentence", features=FeatureMatcher(type="weight"))) >>

            token_filter.repeat(0, 2) >>

            (imperial_weight | (metric_weight >> metric_weight_units)) >>

            (AnnAt(type="Lookup", features=FeatureMatcher(minor="weight"))
             .within(type="VarSentence", features=FeatureMatcher(type="weight")).repeat(0, 1)) >>

            AnnAt(type="Lookup", features=FeatureMatcher(major="quantity_change"))

        )
        blocker_1_act = AddAnn(type="Blocked", annset_name="", features={"type": "weight"})
        rule_list.append(Rule(blocker_1, blocker_1_act))

        """
        Blocker 2
        Description: Block things such as:
        Examples: 'patient's BSA (6.0kg)'
        """
        blocker_2 = (
                (context |
                 AnnAt(type="Lookup", features=FeatureMatcher(minor="patient"))
                 .within(type="VarSentence", features=FeatureMatcher(type="weight"))) >>

                token_filter.repeat(0, 2) >>

                Or(AnnAt(type="Lookup", features=FeatureMatcher(minor="height")),
                    AnnAt(type="Lookup", features=FeatureMatcher(minor="body_surface_area"))) >>

                Or(AnnAt(type="Token", features=FeatureMatcher(kind="punctuation")),
                   AnnAt(type="Token", features=FeatureMatcher(kind="symbol"))).repeat(0, 1) >>

                (imperial_weight | (metric_weight >> metric_weight_units))
        )
        blocker_2_act = AddAnn(type="Blocked", annset_name="", features={"type": "weight"})
        rule_list.append(Rule(blocker_2, blocker_2_act))

        """
        Blocker 3
        Description: Block things such as:
        Examples: 'the patient's weight decreased 7 stone' or 'patient admits to putting at least 3 stone of weight on'
        """
        blocker_3 = (
                (context |
                 AnnAt(type="Lookup", features=FeatureMatcher(minor="patient"))
                 .within(type="VarSentence", features=FeatureMatcher(type="weight"))) >>

                token_filter.repeat(0, 8) >>

                AnnAt(type="Lookup", features=FeatureMatcher(major="quantity_change")) >>

                token_filter.repeat(0, 2) >>

                (imperial_weight | (metric_weight >> metric_weight_units)) >>

                token_filter.repeat(0, 2) >>

                AnnAt(type="Lookup", features=FeatureMatcher(minor="preposition")).repeat(0, 1)
        )
        blocker_3_act = AddAnn(type="Blocked", annset_name="", features={"type": "weight"})
        rule_list.append(Rule(blocker_3, blocker_3_act))

        """
        PatientWeight
        Description: Weight
        Example:v
        """
        wt_sent_pat = (
            (context |
             AnnAt(type="Lookup", features=FeatureMatcher(minor="patient"), name="context")
             .within(type="VarSentence", features=FeatureMatcher(type="weight"))) >>

            token_filter.repeat(0, 8) >>

            (imperial_weight | (metric_weight >> metric_weight_units))
        )
        wt_sent_act = AddAnn(type="weight", features=ParseNumericUnits(name_value="value",
                                                                       name_units="units",
                                                                       var_name=self.var_name,
                                                                       mode=self.outset_name,
                                                                       silent_fail=True))
        rule_list.append(Rule(wt_sent_pat, wt_sent_act))

        """
        PatientWeight
        Description: Weight
        Example: 'weight is 170'
        """
        wt_sent_pat_2 = (
                context >>

                AnnAt().repeat(0, 1) >>

                Lookahead(metric_weight, Or(AnnAt().notat(type="Units"),
                                            AnnAt(type="Split")))
        )
        wt_sent_act_2 = AddAnn(type="weight", features=ParseNumericUnits(name_value="value",
                                                                         name_units=None,
                                                                         var_name=self.var_name,
                                                                         mode=self.outset_name,
                                                                         silent_fail=True))
        rule_list.append(Rule(wt_sent_pat_2, wt_sent_act_2))

        return rule_list


