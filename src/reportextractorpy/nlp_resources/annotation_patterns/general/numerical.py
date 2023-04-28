from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import AnnAt, Seq, Text
from gatenlp.pam.pampac import AddAnn
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self):
        self.var_name = ""
        self.descriptor = NotImplemented
        self.outset_name = ""
        self.included_annots = [("", "Numeric")]
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

        rule_list = [Rule(pattern_2, action_2),
                     Rule(pattern_1, action_1),
                     Rule(pattern_3, action_3),
                     Rule(pattern_4, action_4)]

        return rule_list
    # Phase: CleanNumeric
    # Input: Numeric Units Token Split
    # Options: control=Appelt negationGrouping=false
    # /*
    #  * Description:
    #  * Here we retag split numeric values e.g. 1m 80cm ({Numeric}{Units}{Numeric}{Units}) becomes 1.8m {Numeric}{Units}
    #  * To keep it compatible with the Context:Numeric:Units matching we assign the 'value' feature of the metre annotation
    #  * to a combination of the metre and cm; then remove annots from the '80' and the 'cm' so they effectively get ignored.
    #  * is correct.
    #  */
    # Rule: split_metric_length
    # (
    # 	({Numeric}):metres
    # 	({Units.minorType == "m"})
    # 	({Numeric}):cm
    # 	({Units.minorType == "cm"})?
    #
    # ):split_metric
    # -->
    # :split_metric{
    #
    # 	String metres_str = stringFor(doc, bindings.get("metres"));
    # 	String cm_str     = bindings.get("cm")!=null ? stringFor(doc, bindings.get("cm")) : "0";
    # 	String value = null;
    # 	try {
    # 		Double metres = Double.parseDouble(metres_str);
    # 		Double cm     = Double.parseDouble(cm_str);
    # 		metres = metres + (cm / 100.0);
    # 		value = metres.toString();
    # 	}catch(Exception e) {
    # 		return;
    # 	}
    # 	FeatureMap newFeatures = Factory.newFeatureMap();
    # 	newFeatures.put("value", value);
    # 	newFeatures.put("type", "split_value");
    # 	outputAS.add(bindings.get("metres").firstNode(),bindings.get("metres").lastNode(),"Numeric", newFeatures);
    #
    #
    # 	// Since now the data lives in the new Numeric annotation's feature, we can clean up and remove the Numeric / Units annots
    # 	AnnotationSet splitMetricAnnot = bindings.get("split_metric");
    #
    # 	FeatureMap fm_double = Factory.newFeatureMap();
    # 	fm_double.put("type", "double");
    # 	AnnotationSet doubleWithin = inputAS.get("Numeric", fm_double).getContained(
    # 			splitMetricAnnot.firstNode().getOffset(),
    # 			splitMetricAnnot.lastNode().getOffset());
    # 	inputAS.removeAll(doubleWithin);
    #
    # 	FeatureMap fm_integer = Factory.newFeatureMap();
    # 	fm_integer.put("type", "integer");
    # 	AnnotationSet integerWithin = inputAS.get("Numeric", fm_integer).getContained(
    # 			splitMetricAnnot.firstNode().getOffset(),
    # 			splitMetricAnnot.lastNode().getOffset());
    # 	inputAS.removeAll(integerWithin);
    #
    # 	FeatureMap fm_cm = Factory.newFeatureMap();
    # 	fm_cm.put("minorType", "cm");
    # 	AnnotationSet cmUnitsWithin = inputAS.get("Units", fm_cm).getContained(
    # 			splitMetricAnnot.firstNode().getOffset(),
    # 			splitMetricAnnot.lastNode().getOffset());
    # 	inputAS.removeAll(cmUnitsWithin);
    # }


