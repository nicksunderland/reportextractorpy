from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator, GetNumberFromText, RemAnn
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
        self.included_annots = [("", ["Numeric", "Units"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        super().__init__(**self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        # Numeric annotations from within other Numeric annotations with a 'kind' other than 'raw_text'
        numeric_in_numeric = AnnAt(type="Numeric", name="remove_tag").within(type='Numeric', features=dict(kind=re.compile('^(?!raw_text$).*')))

        # Numeric annotations from within other annotations type (except Numeric and sentences)
        numeric_in_other = AnnAt(type="Numeric", name="remove_tag").within(type=re.compile('^(?!Numeric$|Sentence$).*'))

        # The remove action
        action_remove = RemAnn(name="remove_tag")

        return [Rule(numeric_in_numeric, action_remove),
                Rule(numeric_in_other, action_remove)]


#
# Phase: CleanCategorical
# Input: Categorical
# Options: control=Appelt negationGrouping=false
# /*
#  * Description:
#  * Here we remove units within Categorical annotations
#  * e.g. 'is non dilated'
#  * is         -->{Unit, minorType=="positive_assertion"}
#  * non        -->{Unit, minorType=="negative_assertion"}
#  * dilated    -->{Categorical}
#  * non dilated-->{Categorical}
#  * becomes is{Unit} non dilated{Categorical}
#  */
# Rule: clean_categorical
# Priority: 100
# (
# 	{Categorical}
# ):categorical
# -->
# {
# 	AnnotationSet thisCategoricalAnnot = bindings.get("categorical"); // this annotation above
# 	AnnotationSet unitsWithin          = inputAS.get("Units").getContained(
# 											thisCategoricalAnnot.firstNode().getOffset(),
# 											thisCategoricalAnnot.lastNode().getOffset()); // any Units annotations within
# 	AnnotationSet categoricalWithin1   = inputAS.get("Categorical").getContained(
# 											thisCategoricalAnnot.firstNode().getOffset(),
# 											thisCategoricalAnnot.lastNode().getOffset()-1);
# 	AnnotationSet categoricalWithin2   = inputAS.get("Categorical").getContained(
# 											thisCategoricalAnnot.firstNode().getOffset()+1,
# 											thisCategoricalAnnot.lastNode().getOffset());
# 	AnnotationSet anatomyWithin        = inputAS.get("Anatomy").getContained(
# 											thisCategoricalAnnot.firstNode().getOffset(),
# 											thisCategoricalAnnot.lastNode().getOffset());
#
# 	inputAS.removeAll(unitsWithin);
# 	inputAS.removeAll(categoricalWithin1);
# 	inputAS.removeAll(categoricalWithin2);
# 	inputAS.removeAll(anatomyWithin);
#
# }