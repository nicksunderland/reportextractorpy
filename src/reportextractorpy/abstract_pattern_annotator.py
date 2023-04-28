from abc import ABC, abstractmethod
from typing import List, Tuple

from gatenlp.pam.pampac import PampacAnnotator, Pampac, Rule, Result, actions, Getter, PampacParser, Success, Failure
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures, RemoveAnn
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase


class AbstractPatternAnnotator(ABC):

    def __init__(self,
                 outset_name: str = NotImplemented,
                 rule_list: List[Rule] = NotImplemented,
                 var_name: str = NotImplemented,
                 templates: List[dict] = NotImplemented,
                 included_annots: str | List[str | Tuple[str, str | List[str]]] = NotImplemented,
                 pampac_skip: str = NotImplemented,
                 pampac_select: str = NotImplemented,
                 **kwargs):

        self.outset_name = outset_name
        self.rule_list = rule_list
        self.var_name = var_name
        self.templates = templates
        self.included_annots = included_annots
        self.pampac_skip = pampac_skip
        self.pampac_select = pampac_select

    def get_pampac_annotator(self) -> PampacAnnotator:
        # PAMPAC matcher
        pampac = Pampac(*self.rule_list, skip=self.pampac_skip, select=self.pampac_select)
        # Init the Annotator
        anntor = PampacAnnotator(pampac, annspec=self.included_annots, outset_name=self.outset_name)
        # return
        return anntor

    def __iter__(self):
        # if no templates just return self
        if self.templates is NotImplemented:
            yield self.get_pampac_annotator()
        # else return a generator of this class instances, instantiated with
        # the attributes in each template
        else:
            for template in self.templates:
                # add the attributes in the template to self (and overwrite if
                # already present); regenerate the rules and then create the
                # annotator and return in
                attr = dict(list(self.__dict__.items()) + list(template.items()))
                self.__dict__.update(attr)
                self.rule_list = self.gen_rule_list()
                yield self.get_pampac_annotator()

    @abstractmethod
    def gen_rule_list(self) -> List[Rule]:
        pass


