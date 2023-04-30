import inspect
from abc import ABC, abstractmethod
from typing import List, Tuple
import re
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

        self.validate_rules()
        self.outset_name = outset_name
        self.rule_list = rule_list
        self.var_name = var_name
        self.templates = templates
        self.included_annots = included_annots
        self.pampac_skip = pampac_skip
        self.pampac_select = pampac_select

    def validate_rules(self):
        # The annotation types used in the code
        source_code = inspect.getsource(self.gen_rule_list)
        code_type_matches = re.findall(r'(?<!AddAnn)\s{0,2}\(\s{0,2}type\s{0,2}=\s{0,2}[\"\'](.+?)[\"\']', source_code)
        code_types = set(code_type_matches)

        # The input annotation types specified
        input_types = set()
        if isinstance(self.included_annots, str):
            pass  # name of annotation set, going to use all annotations
        elif all(isinstance(c, str) for c in self.included_annots):
            pass  # names of annotation sets, going to use all annotations
        elif all(isinstance(c, tuple) for c in self.included_annots):
            for tup in self.included_annots:
                arg2 = tup[1]
                if isinstance(arg2, str):
                    input_types.add(arg2)
                elif all(isinstance(c, str) for c in arg2):
                    for s in arg2:
                        input_types.add(s)

        if not all(check in input_types for check in code_types):
            raise Exception(
                f'Annotations types found that are not present in the input types\n'
                f'\tModule: \'{self.__module__}\'\n'
                f'\tInput: {input_types}\n'
                f'\tFound: {code_types}'
            )

        if not all(check in code_types for check in input_types):
            print(f'\033[93m Warning: annotation types referenced in input but not found in code\n'
                  f'\tModule: \'{self.__module__}\'\n'
                  f'\tInput: {input_types}\n'
                  f'\tFound: {code_types} \033[0m')

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


