from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric, RemoveAnnAll, GetList
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Seq, Text, Lookahead, RemoveAnn, AddAnn, Or
from gatenlp.pam.matcher import FeatureMatcher
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self):
        self.var_name = ""
        self.descriptor = NotImplemented
        self.outset_name = ""
        self.included_annots = [("", ["Numeric", "Units", "Lookup", "Token", "Split"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:

        # numeric ranges rule
        pattern_2 = Seq(AnnAt(type="Numeric", name="value_1"),
                        Text(text=re.compile('(?:[-]|to[-]?)(?:\s[a]\s)?(?:max|min(?:imum)?)?(?:\sof)?', flags=re.I)),
                        AnnAt(type="Numeric", name="value_2"))
        action_2 = AddAnn(type="Numeric", features={"value": GetNumberFromNumeric(name_1="value_1", name_2="value_2"),
                                                    "kind": "numeric_range",
                                                    "value_1": GetNumberFromNumeric(name_1="value_1"),
                                                    "value_2": GetNumberFromNumeric(name_2="value_2"),
                                                    "func": "averaged"})

        # fractions rule
        pattern_1 = Seq(AnnAt(type="Numeric", name="value_1"),
                        Text(text=re.compile(r'/')),
                        AnnAt(type="Numeric", name="value_2"))
        action_1 = AddAnn(type="Numeric", features={"value": GetNumberFromNumeric(name_1="value_1",
                                                                                  name_2="value_2",
                                                                                  func=lambda x, y: float(x)/float(y)),
                                                    "kind": "fraction"})

        # orthogonal number rule
        pattern_3 = Seq(AnnAt(type="Numeric", name="value_1"),
                        Text(text=re.compile(r'\s?(?:x|by)\s?')),
                        AnnAt(type="Numeric", name="value_2"))
        action_3 = AddAnn(type="Numeric", features={"value_1": GetNumberFromNumeric(name_1="value_1"),
                                                    "value_2": GetNumberFromNumeric(name_2="value_2"),
                                                    "kind": "orthogonal_numbers"})

        # numeric categories / type description e.g. type 2 MI
        pattern_4 = Seq(Text(text=re.compile(r'type\s?', re.I)),
                        AnnAt(type="Numeric", name="value"))
        action_4 = AddAnn(type="Lookup", features={"value": GetNumberFromNumeric(name_1="value"),
                                                   "kind": "numeric_category"})

        # split metric length
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

        # Tag references to specific images or frames and remove the numeric tag e.g. frame 4 & 5 & 6, or images 4, 6
        frame_reference_pattern = Seq(AnnAt(type="Lookup", features=FeatureMatcher(major="image_frame")),
                                      Seq(AnnAt(type="Numeric", name="frame_num"),
                                          AnnAt(type="Token", features=FeatureMatcher(kind="punctuation")).notcoextensive(type="Split").repeat(0,1)
                                          ).repeat(1, 5))

        frame_reference_action = AddAnn(type="Lookup", features={"value": GetList(name="frame_num"),
                                                                 "major": "image_frame_value",
                                                                 "minor": "image_frame_value"})
        remove_action_2 = RemoveAnnAll(name="frame_num", annset_name="", silent_fail=True)

        rule_list = [Rule(pattern_2, action_2),
                     Rule(pattern_1, action_1),
                     Rule(pattern_3, action_3),
                     Rule(pattern_4, action_4),
                     Rule(split_length_pattern, split_length_action_1, remove_action_1),
                     Rule(frame_reference_pattern, frame_reference_action, remove_action_2)]

        return rule_list

    """
    
    Phase: RelationalDistance
    Input: Numeric Token Lookup Anatomy Units Split
    Options: control=Brill negationGrouping=false
    /*
     * Description:
     * Tag references to distances in relation to something else, these rarely are the numeric value we want 
     * e.g. the Asc Ao measured 1cm from the StJ is 33mm (we want to tag the 1cm as a relational distance and 
     * the 33mm as a normal integer Numeric annotation which can be found later
     */
    Rule: relational_distance_rule
    (	
        ({Anatomy}):anatomy1
        ({Token, !Split})[0,1]
        {Lookup.majorType == "measure_verb"}
        ({Numeric}):distance
        (({Units.majorType == "length"})?):units
        {Lookup.minorType == "preposition", //e.g. from
            !Token.string ==~ "(at)|(on)"}
        ({Anatomy}):anatomy2
    
    ):relational_distance
    -->
    :relational_distance.Lookup = {	 anatomy1  = :anatomy1.Anatomy.minorType,
                                     anatomy2  = :anatomy2.Anatomy.minorType,
                                     distance  = :distance.Numeric.value,
                                     units     = :units.Units.minorType,
                                     majorType = "relational_distance"},
    :relational_distance{
        inputAS.remove( bindings.get("distance").iterator().next() );
        inputAS.remove( bindings.get("anatomy2").iterator().next() );
        if(bindings.get("units")!=null) {
            inputAS.remove(bindings.get("units").iterator().next());
        }
    }
    
    """




