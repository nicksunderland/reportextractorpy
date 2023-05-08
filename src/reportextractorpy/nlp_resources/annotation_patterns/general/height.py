from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric, ParseNumericUnits
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Seq, Text, N, Lookahead, Ann, Or
from gatenlp.pam.matcher import IfNot, FeatureMatcher, AnnMatcher, isIn, FeatureEqMatcher
from gatenlp.pam.pampac import AddAnn, Rule, GetText, UpdateAnnFeatures, GetAnn
from typing import List
import re


class TagVarSentence(AbstractPatternAnnotator):
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
        Description: Tag sentences that contain a mention of height, or simply 'patient',
        Example: 'height is 150cm', 'the patient is 159cm'
        """
        ht_sent_pat = Or(AnnAt(type="Sentence")
                         .covering(type="Lookup", features=FeatureMatcher(minor="height"))
                         .notcovering(type="Anatomy"),
                         AnnAt(type="Sentence")
                         .covering(type="Lookup", features=FeatureMatcher(minor="patient"))
                         .notcovering(type="Anatomy"))
        ht_sent_act = AddAnn(type="VarSentence", features={"type": "height"})
        rule_list.append(Rule(ht_sent_pat, ht_sent_act))
        return rule_list


class PatientHeight(AbstractPatternAnnotator):
    def __init__(self, outset_name):
        self.var_name = "height"
        self.outset_name = outset_name
        self.included_annots = [("", ["Token", "VarSentence", "Anatomy", "Numeric", "Units", "Lookup",
                                      "ImperialMeasurement", "ReportSection", "Measurement", "Categorical"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []
        """
        PatientHeight
        Description:
        Example: 'height is 150cm', 'the patient is 159cm'
        """
        """
        Macro: CONTEXT
        """
        context = \
            AnnAt(type="Lookup", features=FeatureMatcher(minor="height"), name="context")\
            .within(type="VarSentence", features=FeatureMatcher(type="height"))

        """
        Macro: FILTER
        """
        token_filter = \
            AnnAt(type="Token")\
            .within(type="VarSentence", features=FeatureMatcher(type="height"))\
            .notat(type="Lookup", features=FeatureMatcher(minor="indexed"))\
            .notat(type="ReportSection")\
            .notat(type="Anatomy")\
            .notat(type="Measurement")

        """
        Macro: METRIC_LENGTH
        """
        metric_length = AnnAt(type="Numeric", name="value")\
            .within(type="VarSentence", features=FeatureMatcher(type="height"))

        """        
        Macro: IMPERIAL_LENGTH
        """
        imperial_length = \
            AnnAt(type="ImperialMeasurement", features=FeatureMatcher(major="length"), name="value")\
            .within(type="VarSentence", features=FeatureMatcher(type="height"))

        """
        Macro: METRIC_LENGTH_UNITS
        """
        metric_length_units = \
            AnnAt(type="Units", features=FeatureMatcher(major="length"), name="units")\
            .within(type="VarSentence", features=FeatureMatcher(type="height"))
        #how to do this???    !Units.minorType == "mm"}

        """
        PatientHeight
        Description: This rule allows more stuff between the context and value, but enforces the units (metric)
        Example: 'height is loads of other text 170cm' 
        """
        ht_sent_pat = (
            (context |
             AnnAt(type="Lookup", features=FeatureMatcher(minor="patient"), name="context")
             .within(type="VarSentence", features=FeatureMatcher(type="height"))) >>

            token_filter.repeat(0, 8) >>

            (imperial_length | (metric_length >> metric_length_units))
        )
        ht_sent_act = AddAnn(type="height", features=ParseNumericUnits(name_value="value",
                                                                       name_units="units",
                                                                       silent_fail=True))
        rule_list.append(Rule(ht_sent_pat, ht_sent_act))

        """
        PatientHeight
        Description: No units but definitely relating to height
        Example: 'height is 170'
        """
        ht_sent_pat_2 = (
                context >>

                token_filter.repeat(0, 1) >>

                Lookahead(metric_length, AnnAt().notat(type="Units"))

        )
        ht_sent_act_2 = AddAnn(type="height", features=ParseNumericUnits(name_value="value",
                                                                         name_units=None,
                                                                         silent_fail=True))
        rule_list.append(Rule(ht_sent_pat_2, ht_sent_act_2))

        return rule_list
