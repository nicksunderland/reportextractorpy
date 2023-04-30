from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Seq, Text, N, Lookahead, Ann, Or
from gatenlp.pam.matcher import IfNot, FeatureMatcher, AnnMatcher, isIn, FeatureEqMatcher
from gatenlp.pam.pampac import AddAnn
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self):
        self.var_name = ""
        self.outset_name = ""
        self.included_annots = [("", ["Numeric", "Token", "Units"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:

        # measurements in feet and inches (allowing a token inbetween, e.g. comma or fullstop)
        # optional inches units
        pattern_1 = Seq(
                        # Numeric annotation
                        AnnAt(type="Numeric", name="value_1"),
                        # Units annotation
                        AnnAt(type="Units", features=FeatureMatcher(minor="feet")),
                        # Optional sequence of joining phrase (optional) & numeric, followed by an optional inches
                        # unit (lookahead to check units aren't related to mass first before capturing)
                        Seq(Lookahead(parser=Seq(AnnAt(features=FeatureMatcher(text=re.compile('[&,.]|and', flags=re.I))).repeat(0, 1),
                                                 AnnAt(type="Numeric", name="value_2")),
                                      laparser=AnnAt().notoverlapping(type="Units", features=FeatureMatcher(major="mass"))),
                            AnnAt(type="Units", features=FeatureMatcher(minor="inches")).repeat(0, 1)).repeat(0, 1))

        action_1 = AddAnn(type="ImperialMeasurement", features={"major": "length",
                                                                "feet": GetNumberFromNumeric(name_1="value_1"),
                                                                "inches": GetNumberFromNumeric(name_2="value_2", silent_fail=True)})

        # measurements in feet and inches (allowing a token inbetween, e.g. comma or fullstop)
        # optional feet units
        pattern_2 = Seq(AnnAt(type="Numeric", name="value_1"),
                        AnnAt(type="Units", features=FeatureMatcher(minor="feet")).repeat(0, 1),
                        AnnAt(type="Numeric", name="value_2"),
                        AnnAt(type="Units", features=FeatureMatcher(minor="inches")))

        action_2 = AddAnn(type="ImperialMeasurement", features={"major": "length",
                                                                "feet": GetNumberFromNumeric(name_1="value_1", silent_fail=True),
                                                                "inches": GetNumberFromNumeric(name_2="value_2")})

        # inches only
        pattern_3 = Seq(AnnAt(type="Numeric", name="value_2"),
                        AnnAt(type="Units", features=FeatureMatcher(minor="inches")))

        action_3 = AddAnn(type="ImperialMeasurement", features={"major": "length",
                                                                "feet": GetNumberFromNumeric(name_1="value_1",
                                                                                             silent_fail=True),
                                                                "inches": GetNumberFromNumeric(name_2="value_2")})

        rule_list = [Rule(pattern_1, action_1),
                     Rule(pattern_2, action_2),
                     Rule(pattern_3, action_3)]

        return rule_list

#
# Phase: TagImperialWeight
# Input: Numeric Units Token Split
# Options: control=Appelt negationGrouping=false
# /*
#  * Description:
#  * Tag imperial measurements in stone and pounds (allowing a token inbetween, e.g. comma or fullstop)
#  */
# Rule: imperial_weight_0
# (
# 	(({Numeric}{Units.minorType == "stone"} | {Token.string ==~ "1{1,2}st"})):stone //need to deal with the fact that 11st is captured as the string '11st' not two strings '11' 'st'
# 	({Token.string ==~ "[&,.]|(and)"})?
# 	({Numeric}):pounds
# 	{Units.minorType == "pounds"}
#
# ):imperial_weight
# -->
# :imperial_weight{
#
# 	String stone_str = stringFor(doc, bindings.get("stone"));
# 	stone_str = stone_str.replaceAll("[^\\d]", "");
#
# 	FeatureMap newFeatures = Factory.newFeatureMap();
# 	newFeatures.put("majorType","mass");
# 	newFeatures.put("stone", stone_str);
# 	newFeatures.put("pounds", bindings.get("pounds")!=null ? bindings.get("pounds").iterator().next().getFeatures().get("value") : null);
# 	outputAS.add(bindings.get("imperial_weight").firstNode(),bindings.get("imperial_weight").lastNode(),"ImperialMeasurement", newFeatures);
#
# 	// Since now the data lives in the ImperialMeasurement annotation's feature, we can clean up and remove the Numeric / Units annots
# 	AnnotationSet numericWithin = bindings.get("imperial_weight").get("Numeric");
# 	AnnotationSet thisAnnot     = bindings.get("imperial_weight");
# 	AnnotationSet unitsWithin   = inputAS.get("Units", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# 	inputAS.removeAll(numericWithin);
# 	inputAS.removeAll(unitsWithin);
# }
#
# /*
#  * Description:
#  * Tag imperial measurements in stone +/- pounds
#  */
# Rule: imperial_weight_1
# (
# 	(({Numeric}{Units.minorType == "stone"} | {Token.string ==~ "1{1,2}st"})):stone //need to deal with the fact that 11st is captured as the string '11st' not two strings '11' 'st'
# 	(({Numeric})?):pounds
# 	({Units.minorType == "pounds"})?
#
# ):imperial_weight
# -->
# :imperial_weight{
#
# 	String stone_str = stringFor(doc, bindings.get("stone"));
# 	stone_str = stone_str.replaceAll("[^\\d]", "");
#
# 	FeatureMap newFeatures = Factory.newFeatureMap();
# 	newFeatures.put("majorType","mass");
# 	newFeatures.put("stone", stone_str);
# 	newFeatures.put("pounds", bindings.get("pounds")!=null ? bindings.get("pounds").iterator().next().getFeatures().get("value") : null);
# 	outputAS.add(bindings.get("imperial_weight").firstNode(),bindings.get("imperial_weight").lastNode(),"ImperialMeasurement", newFeatures);
#
# 	// Since now the data lives in the ImperialMeasurement annotation's feature, we can clean up and remove the Numeric / Units annots
# 	AnnotationSet numericWithin = bindings.get("imperial_weight").get("Numeric");
# 	AnnotationSet thisAnnot     = bindings.get("imperial_weight");
# 	AnnotationSet unitsWithin   = inputAS.get("Units", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# 	inputAS.removeAll(numericWithin);
# 	inputAS.removeAll(unitsWithin);
# }
#
# /*
#  * Description:
#  * Tag imperial measurements in pounds +/- stone
#  */
# Rule: imperial_weight_2
# (
# 	(((({Numeric})?({Units.minorType == "stone"})?) | ({Token.string ==~ "1{1,2}st"})?)):stone //need to deal with the fact that 11st is captured as the string '11st' not two strings '11' 'st'
# 	({Numeric}):pounds
# 	{Units.minorType == "pounds"}
#
# ):imperial_weight
# -->
# :imperial_weight{
#
#
# 	String stone_str = bindings.get("stone")!=null ? stringFor(doc, bindings.get("stone")) : null;
# 	if(stone_str!=null) {
# 		stone_str = stone_str.replaceAll("[^\\d]", "");
# 	}
#
# 	FeatureMap newFeatures = Factory.newFeatureMap();
# 	newFeatures.put("majorType","mass");
# 	newFeatures.put("stone", stone_str);
# 	newFeatures.put("pounds", bindings.get("pounds").iterator().next().getFeatures().get("value"));
# 	outputAS.add(bindings.get("imperial_weight").firstNode(),bindings.get("imperial_weight").lastNode(),"ImperialMeasurement", newFeatures);
#
# 	// Since now the data lives in the ImperialMeasurement annotation's feature, we can clean up and remove the Numeric / Units annots
# 	AnnotationSet numericWithin = bindings.get("imperial_weight").get("Numeric");
# 	AnnotationSet thisAnnot     = bindings.get("imperial_weight");
# 	AnnotationSet unitsWithin   = inputAS.get("Units", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# 	inputAS.removeAll(numericWithin);
# 	inputAS.removeAll(unitsWithin);
# }