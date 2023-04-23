from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Or, N
from gatenlp.pam.pampac import AddAnn
from typing import List
import re


class SentenceTokenizer(AbstractPatternAnnotator):

    def __init__(self):
        super().__init__(
            annotator_outset_name="",  # add back to default annotation set ""
            rule_list=self.gen_rule_list(),
            var_name="",
            included_annots="",
            pampac_skip="longest",
            pampac_select="first")

    def gen_rule_list(self) -> List[Rule]:
        pattern_sent = N(Or(AnnAt(type=re.compile(r'^(?!Split$)')),
                            AnnAt(type="Split").within(type=re.compile(r'^(?!Split$)'))), min=1, max=40)
        action_sent = AddAnn(type="Sentence")
        rule_sent = Rule(pattern_sent, action_sent)

        return [rule_sent]