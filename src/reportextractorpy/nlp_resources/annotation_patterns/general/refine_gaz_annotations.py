from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from gatenlp.pam.pampac import Rule, pampac_parsers
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List
import re


class RefineAnnotations(AbstractPatternAnnotator):

    def __init__(self, outset_name):
        self.var_name = ""
        self.outset_name = ""
        self.included_annots = [("", ["Numeric", "Units"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []

        # Numeric annotations from within other Numeric annotations with a 'kind' other than 'raw_text'
        numeric_in_numeric = AnnAt(type="Numeric", name="remove_tag").within(type='Numeric', features=dict(kind=re.compile('^(?!raw_text$).*')))

        # Numeric annotations from within other annotations type (except Numeric and sentences)
        numeric_in_other = AnnAt(type="Numeric", name="remove_tag").within(type=re.compile('^(?!Numeric$|Sentence$).*'))

        # The remove action
        action_remove = RemoveAnn(name="remove_tag", annset_name="")

        # Add to rules
        rule_list.append(Rule(numeric_in_numeric, action_remove))
        rule_list.append(Rule(numeric_in_other, action_remove))

        """
        Clean categorical annotations 
        Description: Here we remove units within Categorical annotations
        Example: 'is non dilated'
            is         -->{Unit, minorType=="positive_assertion"}
            non        -->{Unit, minorType=="negative_assertion"}
            dilated    -->{Categorical}
            non dilated-->{Categorical}
        becomes is{Unit} non dilated{Categorical}
        """
        # ?not required?

        # Phase: CleanCategorical
        # Input: Categorical
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

        return rule_list


