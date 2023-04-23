from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List


class Pattern(AbstractPatternAnnotator):

    def __init__(self, mode: str):
        init_vars = {
            "annotator_outset_name": "",
            "rules": self.gen_rule_list(),
            "var_name": "Date",
            "included_annots": [("", ["Token", "SpaceToken", "Split", "Lookup", "Units"])],
            "pampac_skip": "longest",
            "pampac_select": "first",
        }
        super().__init__(**init_vars)

    def gen_rule_list(self) -> List[Rule]:
        #"""Text: this sov 3 cm"""
        pat1 = Seq(Ann("Token", name="context"),
                   Ann("Token", name="value_1"),
                   Ann("Token", name="units"), name="testing")
            #,
              #     name="var_name")

        rule1 = Rule(pat1, self.action_v1v2unit_match, priority=0)

        return [rule1]


# Rule: numeric_ranges_rule
# Priority: 99
# (
# 	({Token.kind == "number"}({Token.string ==~ "[.,]"}{Token.kind == "number"})?):lo
# 		({SpaceToken})?
# 			({Units})?
# 				({SpaceToken})?
# 	({Token.string ==~ "(?i)[-]|(to)"})
# 		({SpaceToken}{Token.string ==~ "(?i)a"})?
# 			({SpaceToken}{Token.string ==~ "(?i)(max)|(min)"})?
# 				({SpaceToken}{Token.string ==~ "(?i)of"})?
# 		({SpaceToken})?
# 	({Token.kind == "number"}({Token.string ==~ "[.,]"}{Token.kind == "number"})?):hi
#
#
# 	//33 mm to a max 40 mm
#
# ):numeric_range
# -->
# :numeric_range{
#
# 	String lo_str = stringFor(doc, bindings.get("lo"));
# 	String hi_str = stringFor(doc, bindings.get("hi"));
# 	lo_str = lo_str.replace(",", ".");
# 	hi_str = hi_str.replace(",", ".");
# 	String value  = null;
# 	try {
# 		Double lo = Double.parseDouble(lo_str);
# 		Double hi = Double.parseDouble(hi_str);
# 		Double av = (lo + hi) / 2.0;
# 		value = av.toString();
# 	}catch(Exception e) {
# 		return;
# 	}
#
# 	FeatureMap newFeatures = Factory.newFeatureMap();
# 	newFeatures.put("value", value);
# 	newFeatures.put("hi", hi_str);
# 	newFeatures.put("lo", lo_str);
# 	newFeatures.put("type", "double");
# 	outputAS.add(bindings.get("numeric_range").firstNode(),bindings.get("numeric_range").lastNode(),"Numeric", newFeatures);
# }
#
# /*
#  * Description:
#  * Here we retag orthogonal values as a specific Numeric annotations with 'value1' and 'value2' features
#  */
# Rule: orthogonal_numbers_rule
# Priority: 98
# (
# 	({Token.kind == "number"}({Token.string ==~ "[.,]"}{Token.kind == "number"})?):value1
# 	({SpaceToken})?({Units.majorType == "length"})?({SpaceToken})?
# 	({Token.string ==~ "(?i)(x)|(by)"})
# 	({SpaceToken})?
# 	({Token.kind == "number"}({Token.string ==~ "[.,]"}{Token.kind == "number"})?):value2
#
# ):orthogonal_numbers
# -->
# :orthogonal_numbers{
#
# 	String value1_str = stringFor(doc, bindings.get("value1"));
# 	String value2_str = stringFor(doc, bindings.get("value2"));
# 	value1_str = value1_str.replace(",", ".");
# 	value2_str = value2_str.replace(",", ".");
# 	try {
# 		Double value1 = Double.parseDouble(value1_str);
# 		Double value2 = Double.parseDouble(value2_str);
# 		value1_str = value1.toString();
# 		value2_str = value2.toString();
#
# 	}catch(Exception e) {
# 		return;
# 	}
#
# 	FeatureMap newFeatures = Factory.newFeatureMap();
# 	newFeatures.put("value1", value1_str);
# 	newFeatures.put("value2", value2_str);
# 	newFeatures.put("type", "orthogonal_numbers");
# 	outputAS.add(bindings.get("orthogonal_numbers").firstNode(),bindings.get("orthogonal_numbers").lastNode(),"Numeric", newFeatures);
# }