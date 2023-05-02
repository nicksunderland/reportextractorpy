from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric, GetList
from gatenlp.pam.pampac.actions import RemoveAnnAll, AddAnn, RemoveAnn
from gatenlp.pam.pampac.getters import GetText
from gatenlp.pam.pampac.pampac_parsers import AnnAt, Seq, Text, Lookahead
from gatenlp.pam.pampac.rule import Rule
from gatenlp.pam.matcher import FeatureMatcher
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self):
        self.var_name = ""
        self.descriptor = NotImplemented
        self.outset_name = ""
        self.included_annots = [("", ["Numeric", "Units", "Lookup", "Token", "Split", 'Anatomy'])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)


    def gen_rule_list(self) -> List[Rule]:
        # Rule list
        rule_list = []

        """
        Numeric ranges rule
        Description: tag ranges and return average as the value
        Example: '40-to-60' -> 50
        """
        pattern_2 = Seq(AnnAt(type="Numeric", name="value_1"),
                        Text(text=re.compile('(?i)-?to-?(?=[0-9]| )(?: a )?(?:(?:max|min)(?:imum)?)?(?: of)?')),
                        AnnAt(type="Numeric", name="value_2"))
        action_2 = AddAnn(type="Numeric", features={"value": GetNumberFromNumeric(name_1="value_1", name_2="value_2"),
                                                    "kind": "numeric_range",
                                                    "value_1": GetNumberFromNumeric(name_1="value_1"),
                                                    "value_2": GetNumberFromNumeric(name_2="value_2"),
                                                    "func": "averaged"})
        rule_list.append(Rule(pattern_2, action_2))

        """
        Fractions rule
        Description: tag fractions and convert to float
        Example: '1/4' -> 0.25
        """
        pattern_1 = Seq(AnnAt(type="Numeric", name="value_1"),
                        AnnAt(text="/"),
                        AnnAt(type="Numeric", name="value_2"))
        action_1 = AddAnn(type="Numeric", features={"value": GetNumberFromNumeric(name_1="value_1",
                                                                                  name_2="value_2",
                                                                                  func=lambda x, y: float(x)/float(y)),
                                                    "kind": "fraction"})
        rule_list.append(Rule(pattern_1, action_1))

        """
        Orthogonal number rule
        Description: tag orthogonal numbers and remove the Numeric annotations
        Example: '3cm by 3cm', '4x5cm'
        """
        orthog_pat = Seq(AnnAt(type="Numeric", name="value_1"),
                         AnnAt(type="Units", name="units_1").repeat(0, 1),
                         AnnAt(text=re.compile(r'(?i)x|by')),
                         AnnAt(type="Numeric", name="value_2"),
                         AnnAt(type="Units", name="units_2").repeat(0, 1))

        orthog_act = AddAnn(type="Numeric", features={"value_1": GetNumberFromNumeric(name_1="value_1"),
                                                      "units_1": GetText(name="units_1", silent_fail=True),
                                                      "value_2": GetNumberFromNumeric(name_2="value_2"),
                                                      "units_2": GetText(name="units_2", silent_fail=True),
                                                      "kind": "orthogonal_numbers"})
        orthog_act_2 = RemoveAnnAll(types="Numeric")
        rule_list.append(Rule(orthog_pat, orthog_act, orthog_act_2))

        """
        Numeric categories / description 
        Description: tag categories or number descriptors that are not 'numeric'
        Example: 'type 2 MI'
        """
        pattern_4 = Seq(AnnAt(text=re.compile(r'(?i)type')),
                        AnnAt(type="Numeric", name="value"))
        action_4 = AddAnn(type="Lookup", features={"value": GetNumberFromNumeric(name_1="value"),
                                                   "kind": "numeric_category"})
        rule_list.append(Rule(pattern_4, action_4))

        """
        Split metric length
        Description: Convert split lengths into one numeric value
        Example: '1m 80cm' -> 180cm
        """
        split_length_pattern = Seq(AnnAt(type="Numeric", name="value_1"),
                                   AnnAt(type="Units", features=FeatureMatcher(minor="m"), name="remove"),
                                   Lookahead(AnnAt(type="Numeric", name="value_2"),
                                             AnnAt(type="Units", features=FeatureMatcher(minor="cm"))),
                                   name="split_length")
        split_length_action_1 = AddAnn(type="Numeric", features={"value": GetNumberFromNumeric(name_1="value_1",
                                                                                               name_2="value_2",
                                                                                               func=lambda x, y: float(x)*100 + float(y)),
                                                                 "kind": "split_metric"})
        remove_action_1 = RemoveAnn(name="remove", annset_name="")
        rule_list.append(Rule(split_length_pattern, split_length_action_1, remove_action_1))

        """
        Non-numeric image numbers 
        Description: Tag references to specific images or frames and remove the numeric tag.
        Example: 'frame 4 & 5 & 6, or images 4, 6'
        """
        frame_reference_pattern = Seq(AnnAt(type="Lookup", features=FeatureMatcher(major="image_frame")),
                                      Seq(AnnAt(type="Numeric", name="frame_num"),
                                          AnnAt(type="Token", features=FeatureMatcher(kind="punctuation"))
                                          .notcoextensive(type="Split").repeat(0, 1)
                                          ).repeat(1, 5))

        frame_reference_action = AddAnn(type="Lookup", features={"value": GetList(name="frame_num"),
                                                                 "major": "image_frame_value",
                                                                 "minor": "image_frame_value"})
        remove_action_2 = RemoveAnnAll(names="frame_num", silent_fail=True)
        rule_list.append(Rule(frame_reference_pattern, frame_reference_action, remove_action_2))

        """
        Relational distances 
        Description: tag references to distances in relation to something else, these rarely are the numeric value we 
        want. Below, we want to tag the 1cm as a relational distance and the 33mm as a normal integer Numeric 
        annotation which can be found later.
        Example: 'the Asc Ao measured 1cm from the StJ is 33mm'
        """
        rel_dist_pattern = Seq(AnnAt(type="Anatomy", name="anatomy_1"),
                               AnnAt(type="Token").notat(type=re.compile(r'Split|Lookup')).repeat(0, 1),
                               AnnAt(type="Lookup", features=FeatureMatcher(major="measure_verb")),
                               AnnAt(type="Numeric", name="distance"),
                               AnnAt(type="Units", name="units").repeat(0, 1),
                               AnnAt(type="Lookup", features=FeatureMatcher(minor="preposition"))
                               .notat(type="Token", text=re.compile("^(at|on)$")),
                               AnnAt(type="Token").notat(type="Anatomy").repeat(0, 1),
                               AnnAt(type="Anatomy", name="anatomy_2"))

        rel_dist_action = AddAnn(type="Lookup", features={"anatomy_1": GetText(name="anatomy_1"),
                                                          "anatomy_2": GetText(name="anatomy_2"),
                                                          "distance": GetNumberFromNumeric(name_1="distance"),
                                                          "units": GetText(name="units", silent_fail=True),
                                                          "major": "relational_distance"})
        rel_dist_action_2 = RemoveAnn(name="anatomy_2", annset_name="")
        rel_dist_action_3 = RemoveAnn(name="distance", annset_name="")

        rule_list.append(Rule(rel_dist_pattern, rel_dist_action, rel_dist_action_2, rel_dist_action_3))

        return rule_list




