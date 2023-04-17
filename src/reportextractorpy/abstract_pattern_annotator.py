from abc import ABC, abstractmethod
from typing import List, Tuple
from gatenlp.pam.pampac import PampacAnnotator, Pampac, Rule


class AbstractPatternAnnotator(PampacAnnotator, ABC):

    @abstractmethod
    def __init__(self,
                 rule_list: List[Rule] = None,
                 included_annots: str | List[str | Tuple[str, str] | Tuple[str, List[str]]] = None,
                 pampac_skip: str = None,
                 pampac_select: str = None,
                 annotator_outset_name: str = None):

        self._rule_list = rule_list
        self._included_annots = included_annots
        self._pampac_skip = pampac_skip
        self._pampac_select = pampac_select
        self._annotator_outset_name = annotator_outset_name
        pass

    def append_rule(self, rule: Rule):
        self._rule_list.append(rule)

    def set_rule_list(self, rule_list: List[Rule]):
        self._rule_list = rule_list

    def set_included_annots(self, included_annots: str | List[str | Tuple[str, str] | Tuple[str, List[str]]]):
        self._included_annots = included_annots

    def set_pampac_skip(self, pampac_skip: str):
        self._pampac_skip = pampac_skip

    def set_pampac_select(self, pampac_select: str):
        self._pampac_select = pampac_select

    def set_pampac_annotator_outset_name(self, annotator_outset_name):
        self._annotator_outset_name = annotator_outset_name

    def validator(self):
        print("validating some stuff e.g.: " + self._pampac_select)

    def annotator(self) -> PampacAnnotator:
        # TODO: create this self.validator() function
        pampac = Pampac(*self._rule_list, skip=self._pampac_skip, select=self._pampac_select)
        pattern_annotator = PampacAnnotator(pampac,
                                            annspec=self._included_annots,
                                            outset_name=self._annotator_outset_name)
        return pattern_annotator
