from abc import ABC, abstractmethod
from typing import List, Tuple
from gatenlp.pam.pampac import PampacAnnotator, Pampac, Rule

from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase


class AbstractPatternAnnotator(PampacAnnotator, ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        self._annotator_outset_name = kwargs["annotator_outset_name"]
        self._rule_list = kwargs["rules"]
        self._var_name = kwargs["var_name"]
        self._included_annots = kwargs["included_annots"]
        self._pampac_skip = kwargs["pampac_skip"]
        self._pampac_select = kwargs["pampac_select"]
        self.validator()
        pampac = Pampac(*kwargs["rules"], skip=kwargs["pampac_skip"], select=kwargs["pampac_select"])
        PampacAnnotator.__init__(self, pampac, annspec=kwargs["included_annots"], outset_name=kwargs["annotator_outset_name"])

    @abstractmethod
    def gen_rule_list(self) -> List[Rule]:
        pass

    def validator(self):
        # TODO: create this self.validator() function
        print("validating some stuff e.g.: " + self._pampac_select)
        #included_annots(self, included_annots: str | List[str | Tuple[str, str] | Tuple[str, List[str]]])
        #rule_list: List[Rule]
        #var_name: str
        #pampac_skip: str
        #pampac_select: str
        #annotator_outset_name: str

    def append_rule(self, rule: Rule):
        self._rule_list.append(rule)

    def action_v1v2unit_match(self, succ, context, location):

        if succ.issuccess():
            print("action_v1v2unit_match")
            succ.pprint()

            context_str = GetText(name="context", resultidx=0, matchidx=0)(succ, context, location)
            value_str = GetText(name="value", resultidx=0, matchidx=0)(succ, context, location)
            units_str = GetText(name="units", resultidx=0, matchidx=0)(succ, context, location)

            ann = AddAnn(type=self._var_name,
                         features={"context": context_str,
                                   "value": value_str,
                                   "units": units_str,
                                   "value_1": None,
                                   "value_2": None})
            ann(succ, context, location)

