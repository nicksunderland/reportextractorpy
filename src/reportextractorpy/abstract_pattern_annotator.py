from abc import ABC, abstractmethod
from typing import List, Tuple
from gatenlp.pam.pampac import PampacAnnotator, Pampac, Rule, Result
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase


class AbstractPatternAnnotator(PampacAnnotator, ABC):
    @abstractmethod
    def __init__(self,
                 annotator_outset_name: str,
                 rule_list: List[Rule],
                 var_name: str,
                 included_annots: str | Tuple[str, str] | List[Tuple[str, str|List[str]]],
                 pampac_skip: str,
                 pampac_select: str):

        self._annotator_outset_name = annotator_outset_name
        self._rule_list = rule_list
        self._var_name = var_name
        self._included_annots = included_annots
        self._pampac_skip = pampac_skip
        self._pampac_select = pampac_select

        pampac = Pampac(*self._rule_list,
                        skip=self._pampac_skip,
                        select=self._pampac_select)

        PampacAnnotator.__init__(self,
                                 pampac,
                                 annspec=self._included_annots,
                                 outset_name=self._annotator_outset_name)

    @abstractmethod
    def gen_rule_list(self) -> List[Rule]:
        pass

    def validator(self, kwargs):
        # TODO: create this self.validator() function
        print("validating some stuff e.g.: " + self._pampac_select)

        assert all([hasattr(self, "_annotator_outset_name"),
                    hasattr(self, "_var_name"),
                    hasattr(self, "_included_annots"),
                    hasattr(self, "_pampac_skip"),
                    hasattr(self, "_pampac_select"),
                    hasattr(self, "_rule_list")])

    def append_rule(self, rule: Rule):
        self._rule_list.append(rule)

    @staticmethod
    def sub_match_result(result: Result, name: str):
        try:
            if len(result.matches4name(name)) == 1:
                return result.matches4name(name)[0]
            elif len(result.matches4name(name)) > 1:
                raise IndexError
            else:
                return {}
        except IndexError:
            print("AbstractPatternAnnotator.sub_match_result() returned multiple sub-pattern matches."
                  "Check the annotation pattern doesn't contain duplicate sub-match naming")

    def action_v1v2unit_match(self, success, context, location):

        if success.issuccess():
            print("action_v1v2unit_match")
            success.pprint()

            m = {"context": None,
                 "value": None,
                 "value_1": None,
                 "value_2": None,
                 "units": None}

            for match_result in success:
                for sub_match_name, sub_match_str in m.items():
                    if self.sub_match_result(match_result, sub_match_name):
                        m[sub_match_name] = GetText(name=sub_match_name)(success, context, location)

            if m["value"] is None and all([m["value_1"], m["value_2"]]):
                try:
                    av = (float(m["value_1"]) + float(m["value_2"])) * 0.5
                    m["value"] = str(av)
                except ValueError:
                    print("""ValueError in action_v1v2unit_match():
                             - value_str: {value_str}
                             - value_1_str: {value_1_str}
                             - value_2_str: {value_2_str}
                             - context_str: {context_str}
                             - units_str: {units_str}""".format(value_str=m["value"],
                                                                value_1_str=m["value_1"],
                                                                value_2_str=m["value_2"],
                                                                context_str=m["context"],
                                                                units_str=m["units"]))
            else:
                print("error in action_v1v2unit_match()")

            ann = AddAnn(type=self._var_name, features=m)
            ann(success, context, location)

