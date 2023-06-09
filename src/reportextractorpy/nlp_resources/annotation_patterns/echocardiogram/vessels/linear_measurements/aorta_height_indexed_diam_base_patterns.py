Template: variable_name = "ao_root_diam_ht_idx"
Template: descriptor    = "aortic_root"

Template: variable_name = "ao_sov_diam_ht_idx"
Template: descriptor    = "sinus_of_valsalva"

Template: variable_name = "ao_stj_diam_ht_idx"
Template: descriptor    = "sinotubular_junction"

Template: variable_name = "ao_asc_diam_ht_idx"
Template: descriptor    = "ascending_aorta"


#
# Imports: {
# 	import static gate.Utils.*;
# 	import BHI.ReportExtractor.JapeRhsProcessor;
# }
#
#
#
# Phase: AortaHeightIndexedDiameter
# Input: Token Anatomy Numeric Units Lookup VarSentence Split Categorical BlockedContext
# Options: control=Appelt negationGrouping=false
#
# Macro: CONTEXT
# (
# 	{Anatomy,
# 		Anatomy within {VarSentence.minorType == [descriptor]},
# 		Anatomy notWithin {BlockedContext.type == [variable_name]},
# 		Anatomy.minorType == [descriptor],
# 		Anatomy.minorType != "aortic_root"}
# 	({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string=="/"} | {Token.string==","})?
# )
#
# Macro: CONTEXT_OTHER_AORTA
# (
# 	{Anatomy,
# 		Anatomy within {VarSentence.minorType == [descriptor]},
# 		Anatomy.majorType == "aorta",
# 		Anatomy.minorType != "aortic_root"}
# 	({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string=="/"} | {Token.string==","})?
# )
#
# Macro: CONTEXT_AORTA_ROOT
# (
# 	{Anatomy,
# 		Anatomy within {VarSentence.minorType == [descriptor]},
# 		Anatomy.majorType == "aorta",
# 		Anatomy.minorType == "aortic_root"}
# 	({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string=="/"} | {Token.string==","})?
# )
#
# Macro: FILTER
# (
# 	{Token,
# 		!Anatomy,
# 		!Lookup.majorType == "quantity_change",
# 		!Lookup.majorType == "body_surface_area",
# 		!Lookup.majorType == "normal_range",
# 		!Units.majorType == "z_score",
# 		Token within {VarSentence.minorType == [descriptor]}}
# 	| {Split}
# )
#
# Macro: VALUE
# (
# 	{Numeric,
# 		Numeric within {VarSentence.minorType == [descriptor]},
# 		Numeric.type == "double"} |
# 	{Numeric,
# 		Numeric within {VarSentence.minorType == [descriptor]},
# 		Numeric.type == "integer"}
# )
#
# Macro: UNITS
# (
# 	{Units,
# 		Units within {VarSentence.minorType == [descriptor]},
# 		Units.majorType == "length/length"}
# )
#
# /*
#  * Description:
#  * This is the most common form 'the SoV is dilated at 45mm (22mm/m)'
#  */
# Rule: ao_diam_ht_idx
# Priority: 100
# (
# 	(
# 		((CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
# 		 ((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
# 		 ((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1])) |
# 		(CONTEXT_AORTA_ROOT)
# 	):context
#
# 	( FILTER )[0,20]
#
# 	( VALUE ):value
#
# 	( UNITS ):unit
#
# ):annot
# -->
# :annot.varName = {var_name = [variable_name]},
# :annot{
#
# 	/* Templated strings can only be used with the standard Gate annotation form, not with plain blocks of java code.
# 	 * Therefore we have to annotate using the standard form and then extract the templated string from the annotation's
# 	 * feature map.
# 	 */
# 	AnnotationSet thisAnnot      = bindings.get("annot");
# 	AnnotationSet tmpVarNameAnns = inputAS.get("varName", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# 	String var_name              = (String) tmpVarNameAnns.iterator().next().getFeatures().get("var_name");
# 	inputAS.removeAll(tmpVarNameAnns);
#
# 	/* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# 	 * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# 	 * annotation set).
# 	 */
# 	JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
#
#
# /*
#  * Description:
#  * Of the form 'indexed to height the SOV is dilated at 45mm (22mm/m)'
#  * The units here are optional as we declared that it was indexed to height at the start
#  */
# Rule: ao_diam_ht_idx_2
# Priority: 98
# (
# 	(
# 		{Lookup,
# 			Lookup.majorType == "indexed",
# 			Lookup within {VarSentence.minorType == [descriptor]}}
# 		({Token})?
# 		{Lookup.majorType == "height"}
# 		({Token})?
#
# 		(((CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
# 		  ((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
# 		  ((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1])) |
# 		 (CONTEXT_AORTA_ROOT) )
#
# 	):context
#
# 	( FILTER )[0,20]
#
# 	( VALUE ):value
#
# 	( (UNITS)? ):unit
#
# 	({Token, !Units} | {Split})
#
# ):annot
# -->
# :annot.varName = {var_name = [variable_name]},
# :annot{
#
# 	/* Templated strings can only be used with the standard Gate annotation form, not with plain blocks of java code.
# 	 * Therefore we have to annotate using the standard form and then extract the templated string from the annotation's
# 	 * feature map.
# 	 */
# 	AnnotationSet thisAnnot      = bindings.get("annot");
# 	AnnotationSet tmpVarNameAnns = inputAS.get("varName", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# 	String var_name              = (String) tmpVarNameAnns.iterator().next().getFeatures().get("var_name");
# 	inputAS.removeAll(tmpVarNameAnns);
#
# 	/* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# 	 * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# 	 * annotation set).
# 	 */
# 	JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
#
# /*
#  * Here we allow words like "indexed" or "normalised" without reference to what they are
#  * indexed to, AS LONG AS the units are enforced as length/length (e.g. cm/m) so that we
#  * can infer that they are indexing to height
#  * e.g. indexed SoV = 33mm/m
#  */
# Rule: ao_diam_ht_idx_3
# Priority: 97
# (
# 	(
# 		{Lookup,
# 			Lookup.majorType == "indexed",
# 			Lookup within {VarSentence.minorType == [descriptor]}}
#
# 		( ((CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
# 	       ((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
# 	       ((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1])) |
# 		  (CONTEXT_AORTA_ROOT) )
#
# 	):context
#
# 	( FILTER )[0,30]
#
# 	( VALUE ):value
#
# 	( UNITS ):unit
#
# ):annot
# -->
# :annot.varName = {var_name = [variable_name]},
# :annot{
#
# 	/* Templated strings can only be used with the standard Gate annotation form, not with plain blocks of java code.
# 	 * Therefore we have to annotate using the standard form and then extract the templated string from the annotation's
# 	 * feature map.
# 	 */
# 	AnnotationSet thisAnnot      = bindings.get("annot");
# 	AnnotationSet tmpVarNameAnns = inputAS.get("varName", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# 	String var_name              = (String) tmpVarNameAnns.iterator().next().getFeatures().get("var_name");
# 	inputAS.removeAll(tmpVarNameAnns);
#
# 	/* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# 	 * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# 	 * annotation set).
# 	 */
# 	JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
#
