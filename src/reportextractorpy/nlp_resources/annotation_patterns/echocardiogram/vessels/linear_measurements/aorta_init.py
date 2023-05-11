from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase, FeatureMatcher
from typing import List
import re

"""
The aorta section of the report needs to be tagged first.
Ensure ReportSection phases run first (report_sections.jape)

These phases tag sentences that contain specific aorta references. If the 
sentence following the sentence containing the reference doesn't contain
another Anatomy annotation then this is also captured as it often can 
contain useful information e.g. 'The SoV is 3.2cm. This is not dilated.'
We first tag aorta sentences, then extend the annotations, then run the rest
of the sentence tagging to ensure the extended annots can be used also. 
"""


class TagVarSentenceAorta(AbstractPatternAnnotator):
    """
    Description:
    Sentence that contains 'aorta' phrases.
    We include the Split annotations as this will block additional sentences
    being added if there are multiple return lines between them.
    (i.e. Split.kind=='external' is blocked inbetween sentences)
    """
    def __init__(self, outset_name):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented
        self.templates = NotImplemented
        self.outset_name = ""
        self.included_annots = [("", ["Sentence", "Anatomy", "Split", "SectionHeader"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []

        aorta_sent_pat = (
            AnnAt(type="Sentence")
            .covering(type="Anatomy", features=FeatureMatcher(major="aorta"))
            .notcovering(type="SectionHeader", features=IfNot(FeatureMatcher(minor="aorta"))) >>

            AnnAt(type="Split", features=FeatureMatcher(kind="external"))
            .repeat(0, 1) >>

            AnnAt(type="Sentence")
            .notcovering(type="Anatomy", features=IfNot(FeatureMatcher(major="aorta")))
            .notcovering(type="SectionHeader", features=IfNot(FeatureMatcher(minor="aorta")))
            .repeat(0, 1)

        )
        aorta_sent_act = AddAnn(type="VarSentence", features={"major": "aorta", "minor": "aorta"})
        rule_list.append(Rule(aorta_sent_pat, aorta_sent_act))

        return rule_list


class ExtendAnatomyAnnotations(AbstractPatternAnnotator):
    """
    Description:
    This phase extends the Anatomy annotations based of things found within
    the Aorta Report Section. e.g. "sinuses" could have a number of meanings if
    found elsewhere within a report, however if "sinuses" are found within the
    "AORTA:" report section or a sentence talking about an aorta then it is
    highly likely that it is referring to the sinuses of Valsalva.
    """
    def __init__(self, outset_name):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented
        self.templates = NotImplemented
        self.outset_name = ""
        self.included_annots = [("", ["Token", "ReportSection", "VarSentence", "Lookup", "Anatomy"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []

        """
        Tag single aorta components
        Description: Tag 'root', 'sinus', and 'valsalva' as relating to the aorta if it appears in a
        sentence or report sections about aortas
        Example: 'Something about the aorta. Then talking about a root, sinus, or valsalva' 
        """
        aorta_component_pat_1 = Or(
            AnnAt(text=re.compile(r'(?i)sinus(es)?'))
            .within(type="ReportSection", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="coronary_sinus"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_venosus"))
            .notwithin(type="Lookup", features=FeatureMatcher(minor="cardiac_rhythm")),

            AnnAt(text=re.compile(r'(?i)sinus(es)?'))
            .within(type="ReportSection", features=FeatureMatcher(type="aortic_valve"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="coronary_sinus"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_venosus"))
            .notwithin(type="Lookup", features=FeatureMatcher(minor="cardiac_rhythm")),

            AnnAt(text=re.compile(r'(?i)sinus(es)?'))
            .within(type="VarSentence", features=FeatureMatcher(major="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="coronary_sinus"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_venosus"))
            .notwithin(type="Lookup", features=FeatureMatcher(minor="cardiac_rhythm")),

            AnnAt(text=re.compile(r'(?i)valsalva'))
            .within(type="VarSentence", features=FeatureMatcher(major="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva")),

            AnnAt(text=re.compile(r'(?i)valsalva'))
            .within(type="ReportSection", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva")),

            AnnAt(text=re.compile(r'(?i)valsalva'))
            .within(type="ReportSection", features=FeatureMatcher(type="aortic_valve"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
        )
        aorta_component_act_1 = AddAnn(type="Anatomy", features={"major": "aorta", "minor": "sinus_of_valsalva"})
        rule_list.append(Rule(aorta_component_pat_1, aorta_component_act_1))

        """
        Tag single aorta components
        Description: Tag 'root' and 'sinus' as relating to the aorta if it appears in a
        sentence or report sections about aortas
        Example: 'Something about the aorta. Then talking about a root, sinus, or valsalva' 
        """
        aorta_component_pat_2 = Or(
            AnnAt(text=re.compile(r'(?i)root'))
            .within(type="ReportSection", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_root"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_graft")),

            AnnAt(text=re.compile(r'(?i)root'))
            .within(type="ReportSection", features=FeatureMatcher(type="aortic_valve"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_root"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_graft")),

            AnnAt(text=re.compile(r'(?i)root'))
            .within(type="VarSentence", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_root"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_graft"))
        )
        aorta_component_act_2 = AddAnn(type="Anatomy", features={"major": "aorta", "minor": "aortic_root"})
        rule_list.append(Rule(aorta_component_pat_2, aorta_component_act_2))

        """
        Tag single aorta components
        Description: Tag 'arch' as relating to the aorta if it appears in a
        sentence or report sections about aortas
        Example: 'Something about the aorta. Then talking about an arch' 
        """
        aorta_component_pat_3 = Or(
            AnnAt(text=re.compile(r'(?i)arch'))
            .within(type="ReportSection", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_arch")),

            AnnAt(text=re.compile(r'(?i)arch'))
            .within(type="VarSentence", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="aortic_arch"))
        )
        aorta_component_act_3 = AddAnn(type="Anatomy", features={"major": "aorta", "minor": "aortic_arch"})
        rule_list.append(Rule(aorta_component_pat_3, aorta_component_act_3))

        """
        Tag single aorta components
        Description: Tag 'descending' as relating to the aorta if it appears in a
        sentence or report sections about aortas
        Example: 'Something about the aorta. Then talking about the descending' 
        """
        aorta_component_pat_4 = Or(
            AnnAt(text=re.compile(r'(?i)descending'))
            .within(type="ReportSection", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="descending_aorta")),

            AnnAt(text=re.compile(r'(?i)descending'))
            .within(type="VarSentence", features=FeatureMatcher(type="aorta"))
            .notwithin(type="Anatomy", features=FeatureMatcher(minor="descending_aorta"))
        )
        aorta_component_act_4 = AddAnn(type="Anatomy", features={"major": "aorta", "minor": "descending_aorta"})
        rule_list.append(Rule(aorta_component_pat_4, aorta_component_act_4))

        return rule_list


class TagVarSentenceAortaComponent(AbstractPatternAnnotator):
    """
    Description:
    Tag sentences that contain aortic root references.
    We include the Split annotations as this will block additional sentences
    being added if there are multiple return lines between them
    (i.e. Split.kind=='external' is blocked inbetween sentences)
    """
    def __init__(self, outset_name):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented  # set from templates
        self.descriptor_2 = NotImplemented  # set from templates
        self.templates = [{"descriptor": "aortic_root", "descriptor_2": "aorta"},
                          {"descriptor": "sinus_of_valsalva", "descriptor_2": "sinus_of_valsalva"},
                          {"descriptor": "sinotubular_junction", "descriptor_2": "sinotubular_junction"},
                          {"descriptor": "ascending_aorta", "descriptor_2": "ascending_aorta"}]
        self.outset_name = ""
        self.included_annots = [("", ["Sentence", "Anatomy", "Split", "SectionHeader"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []

        aorta_sent_pat = (
            AnnAt(type="Sentence")
            .covering(type="Anatomy", features=FeatureMatcher(minor=self.descriptor))
            .notcovering(type="SectionHeader", features=IfNot(FeatureMatcher(minor="aorta"))) >>

            AnnAt(type="Split", features=FeatureMatcher(kind="external"))
            .repeat(0, 1) >>

            AnnAt(type="Sentence")
            .notcovering(type="Anatomy", features=IfNot(FeatureMatcher(minor=self.descriptor_2)))  # changed from major to combine into templates, check ok
            .notcovering(type="SectionHeader", features=IfNot(FeatureMatcher(minor="aorta")))
            .repeat(0, 1)

        )
        aorta_sent_act = AddAnn(type="VarSentence", features={"major": "aorta", "minor": self.descriptor})
        rule_list.append(Rule(aorta_sent_pat, aorta_sent_act))

        return rule_list
