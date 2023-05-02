from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Seq, Text, N, Lookahead, Ann, Or
from gatenlp.pam.matcher import IfNot, FeatureMatcher, AnnMatcher, isIn, FeatureEqMatcher
from gatenlp.pam.pampac import AddAnn, Rule
from typing import List
import re


class TagVarSentence(AbstractPatternAnnotator):
    def __init__(self):
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
    def __init__(self):
        self.var_name = "VarSentence"
        self.outset_name = ""
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
        context = AnnAt(type="Lookup",
                        features=FeatureMatcher(minor="height")).within(type="VarSentence",
                                                                        features=FeatureMatcher(type="height"))
        """
        Macro: FILTER
        """
        filter = AnnAt(type="Token")\
            .within(type="VarSentence", features=FeatureMatcher(type="height"))\
            .notat(type="Lookup", features=FeatureMatcher(minor="indexed"))\
            .notat(type="ReportSection")\
            .notat(type="Anatomy")\
            .notat(type="Measurement")
        """
        Macro: METRIC_LENGTH
        """




        """
        PatientHeight
        Description: This rule allows more stuff between the context and value, but enforces the units (metric)
        Example: 'height is loads of other text 170cm' 
        """
        ht_sent_pat = (

            (context | AnnAt(type="Lookup").within(type="VarSentence", features=FeatureMatcher(type="height"))) >>
            filter.repeat(0, 8)

        )

        ht_sent_act = AddAnn(type="TESTING_HEIGHT")
        rule_list.append(Rule(ht_sent_pat, ht_sent_act))


        """
        (	
            ( CONTEXT | {Lookup,
                            Lookup within {VarSentence.type == "height"}, 
                            Lookup.minorType == "patient"} ):context
            
            ( FILTER )[0,8]
            
            ( METRIC_LENGTH ):value
            
            ( METRIC_LENGTH_UNITS ):unit
            
        ):annot 
        --> 
        :annot
        {
            /* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
             * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
             * annotation set).	
             */
            JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", "height", doc, bindings, outputAS);
        }
        
        /*
         * Description:
         * This rule allows more stuff between the context and value, but enforces the units (imperial)
         * e.g. 'height is loads of other text 170cm' 
         */
        Rule: height_2
        Priority: 99
        (	
            ( CONTEXT | {Lookup,
                            Lookup within {VarSentence.type == "height"}, 
                            Lookup.minorType == "patient"} ):context
            
            ( FILTER )[0,8]
            
            ( IMPERIAL_LENGTH ):value
        
        ):annot 
        --> 
        :annot
        {
            /* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
             * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
             * annotation set).	
             */
            JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", "height", doc, bindings, outputAS);
        }
        
        /*
         * Description:
         * e.g. 'height is 170' 
         */
        Rule: height_3
        Priority: 98
        (	
            ( CONTEXT ):context
            
            ( {Token within {VarSentence.type == "height"}} )[0,1]
                    
            ( METRIC_LENGTH ):value
            
            {!Units} // Negative lookahead
        
        ):annot 
        --> 
        :annot
        {
            /* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
             * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
             * annotation set).	
             */
            JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", "height", doc, bindings, outputAS);
        }

        """
        return rule_list
