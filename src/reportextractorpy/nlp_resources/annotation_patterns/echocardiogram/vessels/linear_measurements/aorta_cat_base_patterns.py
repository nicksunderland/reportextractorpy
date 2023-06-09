Template: variable_name = "ao_root_cat"
Template: descriptor    = "aortic_root"

Template: variable_name = "ao_sov_cat"
Template: descriptor    = "sinus_of_valsalva"

Template: variable_name = "ao_stj_cat"
Template: descriptor    = "sinotubular_junction"

Template: variable_name = "ao_asc_cat"
Template: descriptor    = "ascending_aorta"

#
#
# Imports: {
# 	import static gate.Utils.*;
# 	import BHI.ReportExtractor.JapeRhsProcessor;
# }
#
#
#
# Phase: AortaVisualDiameter
# Input: Token Anatomy Numeric Units Lookup VarSentence Split Categorical BlockedContext
# Options: control=Appelt negationGrouping=false
#
# Macro: CONTEXT
# (
# 	{Anatomy,
# 		Anatomy within {VarSentence.minorType == [descriptor]},
# 		Anatomy notWithin {BlockedContext.type == [variable_name]},
# 		Anatomy.minorType == [descriptor]}
# 	({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string==~"[/,-]"})?
# )
#
# Macro: CONTEXT_OTHER_AORTA
# (
# 	{Anatomy,
# 		Anatomy within {VarSentence.majorType == "aorta"},
# 		Anatomy.majorType == "aorta"}
# 	({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string==~"[/,-]"})?
# )
#
# Macro: CONTEXT_AORTA_ROOT
# (
# 	{Anatomy,
# 		Anatomy within {VarSentence.minorType == "aortic_root"},
# 		Anatomy notWithin {Blocked.type == [variable_name]},
# 		Anatomy.majorType == "aorta",
# 		Anatomy.minorType == "aortic_root"}
# 	({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string==~"[/,-]"})?
# )
#
# Macro: FILTER
# (
# 	{Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.minorType == [descriptor]}}
# )
#
# Macro: FILTER_ALLOW_NEG_MODIFIER
# (
# 	{Token,
# 		!Anatomy,
# 		!Categorical.minorType != "negative_modifier",
# 		Token within {VarSentence.minorType == [descriptor]}}
# )
#
# Macro: FILTER_ALLOW_NEG_AND_SIZE_CAT
# (
# 	{Token,
# 		!Anatomy,
# 		!Categorical.minorType != "negative_modifier",
# 		Token within {VarSentence.minorType == [descriptor]}} |
# 	{Categorical,
# 		Categorical.majorType == "size_category",
# 		Categorical within {VarSentence.minorType == [descriptor]}}
# )
#
# Macro: VALUE_MODIFIER
# (
# 	{Categorical,
# 		Categorical.minorType == "negative_modifier",
# 		Categorical within {VarSentence.minorType == [descriptor]}}
# )
#
# Macro: VALUE
# (
# 	({Categorical,
# 		Categorical.minorType == "dilated",
# 		Categorical within {VarSentence.minorType == [descriptor]}}) |
# 	({Categorical,
# 		Categorical.minorType == "nondilated",
# 		Categorical within {VarSentence.minorType == [descriptor]}})
# )
#
# /*
#  * Description:
#  * Of the forms...
#  * e.g. 'Sinus of Valsalva is not dilated for height'
#  * e.g. 'Sov, Stj, Asc ao are not dilated'
#  * e.g. 'Stj and SOV are not dilated'
#  * e.g. 'Stj and SOV, neither are dilated'
#  * e.g. 'the aortic root there does not appear to be any significant dilatation'
#  * e.g. 'Aortic root:\nNon-dilated.
#  * e.g. 'Sinus of Valsalva is not well seen but doesn't appear dilated for height' (n.b. note the x2 'not'
#  * in this sentence, the first is allowed in the filter, but the second is captured as the VALUE_MODIFIER
#  * as it is in close proximity of the VALUE 'dilated'
#  */
# Rule: ao_cat_1
# Priority: 100
# (
# 	(
# 		  (CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
# 		 ((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
# 		 ((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1])
# 	):context
#
# 	({Token.string==~"[:-]"}{Split.kind=="external"})[0,1]
#
# 	( FILTER_ALLOW_NEG_MODIFIER )[0,20]
#
# 	( (VALUE_MODIFIER)? ):modifier
#
# 	( FILTER )[0,5]
#
# 	( VALUE ):value
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
#  * Description:
#  * Of the form... (we want the height indexed if both are specified)
#  * e.g. 'Sov is not dilated when corrected to BSA, however is dilated when indexed to height.
#  * We need to use a relaxed filter that allows Categorical annotations to pass through in
#  * order to get to the Categorical annotation related to the height indexed mention
#  */
# Rule: ao_cat_2
# Priority: 101
# (
# 	(
# 		((CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
# 		 ((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
# 		 ((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1]))
# 	):context
#
# 	( FILTER_ALLOW_NEG_AND_SIZE_CAT )[0,30]
#
# 	( (VALUE_MODIFIER)? ):modifier
#
# 	( FILTER )[0,2]
#
# 	( VALUE ):value
#
# 	( FILTER )[0,1]
#
# 	{Lookup,
# 		Lookup.majorType == "indexed",
# 		Lookup within {VarSentence.minorType == [descriptor]}}
#
# 	({Lookup,
# 		Lookup.minorType == "preposition",
# 		Lookup within {VarSentence.minorType == [descriptor]}})?
#
# 	{Lookup,
# 		Lookup.majorType == "height",
# 		Lookup within {VarSentence.minorType == [descriptor]}}
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
#  * Description:
#  * Of the forms...
#  * e.g. 'Non-dilated Sov'
#  * e.g. 'Non-dilated Sov, Stj and Asc Ao'
#  * e.g. 'No evidence of significant dilation of the SoV'
#  * e.g. 'Not dilated at the Sov'
#  * e.g. 'Aorta non dilated at the level of the Sov'
#  */
# Rule: ao_cat_3
# Priority: 99
# (
# 	( (VALUE_MODIFIER)? ):modifier
#
# 	( FILTER )[0,3]
#
# 	( VALUE ):value
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		!Lookup.minorType == "conjunction",
# 		Token within {VarSentence.minorType == [descriptor]}} )[0,5]
#
# 	(
# 		(CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
# 		((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
# 		((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1])
# 	):context
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
#  * Of the forms...
#  * e.g. 'Non-dilated aortic root at the Sov'
#  * e.g. 'Non-dilated ascending aorta at the Sov level'
#  * e.g. 'Non dilated proximal aorta to sinus level.'
#  * e.g. 'Non-dilated aortic root at the Sov and Stj'
#  * e.g. 'no significant dilatation of the aortic root at sinus level'
#  * e.g. 'Non dilated proximal aorta (3.1cm at the level of the SOV).'
#  * e.g. 'Non dilated proximal aortic root, Sinus of Valsalva = 3.7cm, sinotubular junction = 3cm, asc ao 3cm.'
#  * e.g. 'Normal dimension of the aortic root. Sinuses 2.8cm'
#  */
# Rule: ao_cat_4
# Priority: 99
# (
# 	( ({Categorical,
# 			Categorical.minorType == "negative_modifier",
# 			Categorical within {VarSentence.majorType == "aorta"}})? ):modifier
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,3]
#
# 	( ({Categorical,
# 			Categorical.minorType == "dilated",
# 			Categorical within {VarSentence.majorType == "aorta"}}) |
# 	  ({Categorical,
# 		  Categorical.minorType == "nondilated",
# 		  Categorical within {VarSentence.majorType == "aorta"}}) ):value
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,3]
#
# 	( CONTEXT_AORTA_ROOT |
# 	  {Anatomy,
# 		Anatomy within {VarSentence.minorType == "ascending_aorta"},
# 		Anatomy.minorType == "ascending_aorta"}	)
#
# 	(	({Token,
# 			!Anatomy,
# 			!Categorical,
# 			Token within {VarSentence.minorType == "aortic_root"}} )[0,5] |
# 		({Token,
# 			!Anatomy,
# 			!Numeric, //dont allow Numeric with ascending aorta mentions as probably a specific prox. asc. ao.
# 			!Categorical,
# 			Token within {VarSentence.minorType == "ascending_aorta"}} )[0,5]  )
#
# 	( {Lookup.minorType == "preposition"} | {Token.string == ","} | {Token.string == "."})
#
# 	( FILTER )[0,5]
#
# 	(
# 			CONTEXT (FILTER)[0,6]                   (CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,2] |
# 		  ((CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,2]  CONTEXT (FILTER)[0,6]) |
# 		  ((CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,1]  CONTEXT (FILTER)[0,6]  (CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,1])
# 	):context
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
#  * Description:
#  * Of the forms...
#  * e.g. 'Aortic root not dilated 4,2cm at the level of the sinuses'
#  * e.g. 'Proximal aorta is not significantly dilated at the level of the sinuses'
#  * e.g. 'Aortic root looks to be significantly dilated 4,2cm at the level of the sinuses'
#  */
# Rule: ao_cat_4b
# Priority: 99
# (
# 	( CONTEXT_AORTA_ROOT |
# 			  {Anatomy,
# 				Anatomy within {VarSentence.minorType == "ascending_aorta"},
# 				Anatomy.minorType == "ascending_aorta"}	)
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,4]
#
# 	( ({Categorical,
# 		Categorical.minorType == "negative_modifier",
# 		Categorical within {VarSentence.majorType == "aorta"}})? ):modifier
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,3]
#
# 	( ({Categorical,
# 			Categorical.minorType == "dilated",
# 			Categorical within {VarSentence.majorType == "aorta"}}) |
# 	  ({Categorical,
# 		  Categorical.minorType == "nondilated",
# 		  Categorical within {VarSentence.majorType == "aorta"}}) ):value
#
# 	(	({Token,
# 			!Anatomy,
# 			!Categorical,
# 			Token within {VarSentence.minorType == "aortic_root"}} )[0,4] |
# 		({Token,
# 			!Anatomy,
# 			!Numeric, //dont allow Numeric with ascending aorta mentions as probably a specific prox. asc. ao.
# 			!Categorical,
# 			Token within {VarSentence.minorType == "ascending_aorta"}} )[0,4]  )
#
#
# 	( {Lookup.minorType == "preposition"} | {Token.string == ","} | {Token.string == "."} )
#
# 	( FILTER )[0,5]
#
# 	(
# 			CONTEXT (FILTER)[0,6]                   (CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,2] |
# 		  ((CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,2]  CONTEXT (FILTER)[0,6]) |
# 		  ((CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,1]  CONTEXT (FILTER)[0,6]  (CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,1])
# 	):context
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
#  * Description:
#  * Of the form...
#  * e.g. 'Non dilated proximal aorta (3.1cm SOV level).'
#  * e.g. 'Non dilated proximal aorta (3.1cm at the SOV, 3.1cm at the STJ, 3.1cm at the Asc Ao level).'
#  * e.g. 'Non dilated proximal aorta (3.1cm at the STJ, 3.1cm at the SOV, 3.1cm at the Asc Ao level).'
#  * e.g. 'Non dilated proximal aorta (3.1cm at the Asc Ao, 3.1cm at the STJ, 3.1cm at the SOV level).'
#  */
# Rule: ao_cat_5
# Priority: 98
# (
# 	( (VALUE_MODIFIER)? ):modifier
#
# 	( FILTER )[0,3]
#
# 	( VALUE ):value
#
# 	( CONTEXT_AORTA_ROOT )
#
# 	( {Token.kind == "punctuation", Token.position == "startpunct"} | {Token.string == ","} )
#
# 	(
# 		(FILTER)[0,6] CONTEXT                   ((FILTER)[0,6] CONTEXT_OTHER_AORTA)[0,2] |
# 	  (((FILTER)[0,6] CONTEXT_OTHER_AORTA)[0,2]  (FILTER)[0,6] CONTEXT ) |
#       (((FILTER)[0,6] CONTEXT_OTHER_AORTA)[0,1]  (FILTER)[0,6] CONTEXT  ((FILTER)[0,6] CONTEXT_OTHER_AORTA)[0,1])
# 	):context
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
#  * Description:
#  * Of the form...
#  * e.g. 'Sinus of Valsalva 4.1cm, proximal ascending aorta 4.3cm, neither are dilated'
#  * e.g. 'SoV 4.1cm, Stj 4.1cm, Asc Ao 4.1cm, all are dilated'
#  * e.g. 'Sinus of Valsalva 4.1cm. Proximal ascending aorta 4.3cm. Neither dilated when related to BSA.
#  * Note the extension of the VarSentence condition to catch Tokens in any sentence relating to the
#  * aorta, instead of just those relating to the [descriptor] part of the aorta - this is to deal with
#  * example #3 above.
#  */
# Rule: ao_cat_6
# Priority: 97
# (
# 	(
# 		CONTEXT (FILTER)[0,6]                   (CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,2] |
# 	  ((CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,2]  CONTEXT (FILTER)[0,6]) |
# 	  ((CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,1]  CONTEXT (FILTER)[0,6]  (CONTEXT_OTHER_AORTA (FILTER)[0,6])[0,1])
# 	):context
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,20]
#
# 	( {Lookup.minorType == "distributive_determiner"} |
# 	  {Lookup.minorType == "demonstrative_determiner"} |
# 	  ({Lookup.minorType == "distributive_determiner",
# 	  		Categorical.minorType == "negative_modifier",
# 	  		Categorical within {VarSentence.majorType == "aorta"}} |
# 	   {Categorical.minorType == "negative_modifier"}):modifier )
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical.minorType != "negative_modifier",
# 		Token within {VarSentence.majorType == "aorta"}} )[0,5]
#
# 	( ({Categorical,
# 		Categorical.minorType == "dilated",
# 		Categorical within {VarSentence.majorType == "aorta"}}) |
# 	  ({Categorical,
# 		Categorical.minorType == "nondilated",
# 		Categorical within {VarSentence.majorType == "aorta"}}) ):value
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
#  * Description:
#  * Of the forms...
#  * e.g. 'Sov to Asc Ao is dilated'
#  * e.g. 'Sov - Asc Ao is nondilated'
#  * This captures the fact that by saying 'SOV to Asc Ao' we are implicitly referencing
#  * the StJ which is inbetween these two structures.
#  */
# Rule: ao_cat_7
# Priority: 96
# (
# 	(
# 		{Anatomy,
# 			Anatomy within {VarSentence.majorType == "aorta"},
# 			Anatomy.minorType == "sinus_of_valsalva"}
# 		{Token,
# 			Token within {VarSentence.majorType == "aorta"},
# 			Token.string ==~ "to|[-]"}
# 		{Anatomy,
# 			Anatomy within {VarSentence.majorType == "aorta"},
# 			Anatomy.minorType == "ascending_aorta"}
# 	):context
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,2]
#
# 	(
# 		({Categorical,
# 			Categorical.minorType == "negative_modifier",
# 			Categorical within {VarSentence.majorType == "aorta"}})?
# 	):modifier
#
# 	(
# 		({Categorical,
# 			Categorical.minorType == "dilated",
# 			Categorical within {VarSentence.majorType == "aorta"}}) |
# 		({Categorical,
# 			Categorical.minorType == "nondilated",
# 			Categorical within {VarSentence.majorType == "aorta"}})
# 	):value
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
# 	/* Don't tag during the aortic root phase, as this phase is reserved for references to the aortic root when
# 	 * the more specific aorta component is not known
# 	 */
# 	if(var_name.contains("ao_root_cat")) {
# 		return;
# 	}
#
# 	/* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# 	 * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# 	 * annotation set).
# 	 */
# 	JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
#
# /*
#  * Description:
#  * Of the forms...
#  * e.g. 'Dilated aortic root from SoV to prox. ascending aorta'
#  * This captures the fact that by saying 'SOV to prox. ascending aorta' we are implicitly referencing
#  * the StJ which is inbetween these two structures. We have to manually set the [variable_name]
#  * to that of the StJ i.e. 'ao_stj_cat'
#  */
# Rule: ao_stj_cat_8
# Priority: 95
# (
# 	(
# 		({Categorical,
# 			Categorical.minorType == "negative_modifier",
# 			Categorical within {VarSentence.majorType == "aorta"}})?
# 	):modifier
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,2]
#
# 	(
# 		({Categorical,
# 			Categorical.minorType == "dilated",
# 			Categorical within {VarSentence.majorType == "aorta"}}) |
# 		({Categorical,
# 			Categorical.minorType == "nondilated",
# 			Categorical within {VarSentence.majorType == "aorta"}})
# 	):value
#
# 	(
# 		({Anatomy,
# 			Anatomy.minorType == "aortic_root",
# 			Anatomy within {VarSentence.majorType == "aorta"}} |
# 		 {Anatomy,
# 			Anatomy.minorType == "ascending_aorta",
# 			Anatomy within {VarSentence.majorType == "aorta"}})
# 		{Lookup.minorType == "preposition"}
# 	)?
#
# 	( {Token,
# 		!Anatomy,
# 		!Categorical,
# 		Token within {VarSentence.majorType == "aorta"}} )[0,3]
#
# 	(
# 		{Anatomy,
# 			Anatomy within {VarSentence.majorType == "aorta"},
# 			Anatomy.minorType == "sinus_of_valsalva"}
# 		{Token,
# 			Token within {VarSentence.majorType == "aorta"},
# 			Token.string ==~ "to|[-]"}
# 		{Anatomy,
# 			Anatomy within {VarSentence.majorType == "aorta"},
# 			Anatomy.minorType == "ascending_aorta"}
# 	):context
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
# 	/* Don't tag during the aortic root phase, as this phase is reserved for references to the aortic root when
# 	 * the more specific aorta component is not known
# 	 */
# 	if(var_name.contains("ao_root_cat")) {
# 		return;
# 	}
#
# 	/* Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# 	 * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# 	 * annotation set).
# 	 */
# 	JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }