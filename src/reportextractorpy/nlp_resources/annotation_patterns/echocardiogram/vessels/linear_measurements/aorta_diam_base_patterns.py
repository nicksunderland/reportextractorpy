from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase
from typing import List
import re


class Pattern(AbstractPatternAnnotator):

    def __init__(self):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented
        self.templates = [{"var_name": "ao_sov",      "descriptor": "sinus_of_valsalva"},
                          {"var_name": "ao_stj_diam", "descriptor": "sinotubular_junction"},
                          {"var_name": "ao_asc_diam", "descriptor": "ascending_aorta"}]
        self.outset_name = "echocardiogram"
        self.included_annots = [("", ["Token", "Anatomy", "Numeric", "Units"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:

        pattern_1 = Seq(AnnAt(type="Anatomy", features=dict(minor=self.descriptor), name="context"),
                        AnnAt(type="Numeric", name="value"),
                        AnnAt(type="Units", features=dict(major="length"), name="units"))

        action_1 = AddAnn(type=self.var_name, features={"context": GetText(name="context"),
                                                        "value": GetNumberFromNumeric(name_1="value"),
                                                        "units": GetText(name="units", silent_fail=True)})

        rule_list = [
            Rule(pattern_1, action_1)
        ]

        return rule_list


#
# Phase: AortaDiameter
# Input: Token
# Anatomy
# Numeric
# Units
# Lookup
# VarSentence
# Split
# Categorical
# BlockedContext
# Options: control = Appelt
# negationGrouping = false
#
# Macro: CONTEXT
# (
#     {Anatomy,
#      Anatomy within {VarSentence.minorType == [descriptor]},
#      Anatomy notWithin {BlockedContext.type == [variable_name]},
#      Anatomy.minorType == [descriptor]}
#     ({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string == "/"} | {
#         Token.string == ","})?
# )
#
# Macro: CONTEXT_OTHER_AORTA
# (
#     {Anatomy,
#      Anatomy within {VarSentence.minorType == [descriptor]},
#      Anatomy.majorType == "aorta",
#      Anatomy.minorType != [descriptor]}
#     ({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string == "/"} | {
#         Token.string == ","})?
# )
#
# Macro: CONTEXT_AORTA_ROOT
# (
#     {Anatomy,
#      Anatomy within {VarSentence.minorType == [descriptor]},
#      Anatomy.majorType == "aorta",
#      Anatomy.minorType == "aortic_root"}
#     ({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string == "/"} | {
#         Token.string == ","})?
# )
#
# Macro: FILTER
# (
#     {Token,
#     !Anatomy,
#     !Units.majorType == "length",
#     !Lookup.majorType == "quantity_change",
#     !Lookup.majorType == "height",
#     !Lookup.majorType == "body_surface_area",
#     !Lookup.majorType == "normal_range",
#     !Units.majorType == "z_score",
#     Token within {VarSentence.minorType ==[descriptor]}}
#     | {Split}
# )
#
# Macro: VALUE
# (
#         {Numeric,
#          Numeric within {VarSentence.minorType == [descriptor]},
#          Numeric.type == "double"} |
#         {Numeric,
#          Numeric within {VarSentence.minorType == [descriptor]},
#          Numeric.type == "integer"}
# )
#
# Macro: UNITS
# (
#     {Units,
#      Units within {VarSentence.minorType == [descriptor]},
#      Units.majorType == "length"}
# )
#
# / *
# *Description:
# *block
# things
# that
# start
# with indexed e.g.'indexed SoV 33mm.'
# * /
# Rule: ao_idx_diam_blocker_1
# Priority: 100
# (
#     {Lookup.majorType == "indexed",
#      Lookup within {VarSentence.minorType == [descriptor]}}
#
#     (CONTEXT):context
#
# ): indexed_diam_blocker
# -->
# :indexed_diam_blocker.Blocked = {type = [variable_name], rule = "ao_idx_diam_blocker_1"},
# :context.BlockedContext = {type = [variable_name], rule = "ao_idx_diam_blocker_1"}
#
# / *
# *Description:
# *This is the
# most
# common
# form:
# *e.g.
# 'the Stj is dilated at 45mm'
# *e.g.
# 'the `Stj and Sov are 3.0cm'
# * /
# Rule: ao_diam_1
# Priority: 100
# (
#     (
#         ((CONTEXT(CONTEXT_OTHER_AORTA)[0, 2]) |
#          ((CONTEXT_OTHER_AORTA)[0, 2] CONTEXT) |
#          ((CONTEXT_OTHER_AORTA)[0, 1] CONTEXT (CONTEXT_OTHER_AORTA)[0, 1]))
# ): context
#
# (FILTER)[0, 15]
#
# (VALUE):value
#
# ((UNITS)? ):unit
#
# ({Token,
# !Anatomy.majorType == "misc_echo_descriptor",
# !Units} | {Split})
#
# ):annot
# -->
# :annot.varName = {var_name = [variable_name]},
# :annot
# {
#
# / * Templated
# strings
# can
# only
# be
# used
# with the standard Gate annotation form, not with plain blocks of java code.
# * Therefore we have to annotate using the standard form and then extract the templated string from the annotation's
# * feature map.
# * /
# AnnotationSet thisAnnot      = bindings.get("annot");
# AnnotationSet tmpVarNameAnns = inputAS.get("varName", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# String var_name              = (String) tmpVarNameAnns.iterator().next().getFeatures().get("var_name");
# inputAS.removeAll(tmpVarNameAnns);
#
# / * Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# * annotation set).
# * /
# JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
#
# / *
# *Description:
# *The
# rule
# captures
# more
# complicated
# phrases
# of
# the
# form:
# *e.g.
# "Aortic root measures 4,2cm at the level of the stj."
# *e.g.
# "Aortic root measures 4,2cm at the level of the sov and stj."
# * /
# Rule: ao_diam_2
# Priority: 99
# (
#     (CONTEXT_AORTA_ROOT)
#
#     (FILTER)[0, 5]
#
#     (VALUE):value
#
# ( (UNITS)? ):unit
#
# {Lookup.minorType == "preposition"}
#
# (FILTER)[0, 5]
#
#     (
#     (CONTEXT(CONTEXT_OTHER_AORTA)[0, 2]) |
#     ((CONTEXT_OTHER_AORTA)[0, 2] CONTEXT) |
#     ((CONTEXT_OTHER_AORTA)[0, 1] CONTEXT (CONTEXT_OTHER_AORTA)[0, 1])
# ):context
#
# ):annot
# -->
# :annot.varName = {var_name = [variable_name]},
# :annot
# {
#
# / * Templated
# strings
# can
# only
# be
# used
# with the standard Gate annotation form, not with plain blocks of java code.
# * Therefore we have to annotate using the standard form and then extract the templated string from the annotation's
# * feature map.
# * /
# AnnotationSet thisAnnot      = bindings.get("annot");
# AnnotationSet tmpVarNameAnns = inputAS.get("varName", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# String var_name              = (String) tmpVarNameAnns.iterator().next().getFeatures().get("var_name");
# inputAS.removeAll(tmpVarNameAnns);
#
# / * Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# * annotation set).
# * /
# JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
#
# / *
# *Description:
# *The
# rule
# captures
# things
# of
# the
# forms:
# *e.g.
# "non-dilated aortic root (33mm Stj level)"
# *e.g.
# "non-dilated aortic root (33mm Sov, 35mm Stj)"
# *e.g.
# "non-dilated aortic root (35mm Stj, 33mm Sov)"
# *e.g.
# "aortic root non dilated (3.5cm stj)"
# *e.g.
# "Non dilated proximal aorta (3.5cm stj)"
# *e.g.
# "Non dilated proximal aorta (3.1cm at the STJ, 3.1cm at the SOV, 3.1cm at the Asc Ao level)"
# * /
# Rule: ao_diam_3
# Priority: 98
# (
#
#     (CONTEXT_AORTA_ROOT)
#
#     ({Categorical})[0, 2]
#
#     {Token.kind == "punctuation", Token.position == "startpunct"}
#
#     (
#     ( VALUE)
# ((UNITS)? )
# ({Lookup.minorType == "preposition"})[0, 1]
# ({Token})[0, 1]
# (CONTEXT_OTHER_AORTA)
# )[0, 2]
#
# (VALUE): value
# ((UNITS)? ):unit
# ({Lookup.minorType == "preposition"})[0, 1]
# ({Token})[0, 1]
# (CONTEXT): context
#
# ):annot
# -->
# :annot.varName = {var_name = [variable_name]},
# :annot
# {
#
# / * Templated
# strings
# can
# only
# be
# used
# with the standard Gate annotation form, not with plain blocks of java code.
# * Therefore we have to annotate using the standard form and then extract the templated string from the annotation's
# * feature map.
# * /
# AnnotationSet thisAnnot      = bindings.get("annot");
# AnnotationSet tmpVarNameAnns = inputAS.get("varName", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# String var_name              = (String) tmpVarNameAnns.iterator().next().getFeatures().get("var_name");
# inputAS.removeAll(tmpVarNameAnns);
#
# / * Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# * annotation set).
# * /
# JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
#
# / *
# *Description:
# *The
# rule
# uses
# a
# more
# relaxed
# filter
# but
# enforces
# the
# units.
# *e.g.STJ
# within
# normal
# limits
# when
# indexed
# for BSA = 4.2cm (indexed 1.9cm/m2)
# * /
# Rule: ao_diam_4
# Priority: 97
# (
#     (CONTEXT):context
#
# ( {Token,
# !Anatomy.minorType !=[descriptor],
# !Units.majorType == "length",
# !Lookup.majorType == "quantity_change",
# Token within {VarSentence.minorType ==[descriptor]}})[0, 10]
#
# (VALUE): value
#
# (UNITS):unit
#
# ({Token,
# !Anatomy.majorType == "misc_echo_descriptor",
# !Units} | {Split})
#
# ):annot
# -->
# :annot.varName = {var_name = [variable_name]},
# :annot
# {
#
# / * Templated
# strings
# can
# only
# be
# used
# with the standard Gate annotation form, not with plain blocks of java code.
# * Therefore we have to annotate using the standard form and then extract the templated string from the annotation's
# * feature map.
# * /
# AnnotationSet thisAnnot      = bindings.get("annot");
# AnnotationSet tmpVarNameAnns = inputAS.get("varName", thisAnnot.firstNode().getOffset(), thisAnnot.lastNode().getOffset());
# String var_name              = (String) tmpVarNameAnns.iterator().next().getFeatures().get("var_name");
# inputAS.removeAll(tmpVarNameAnns);
#
# / * Creation of the processor object does an 'in-place' processing of the annotations found using the above rules.
# * Using the bindings, strings are extracted from the doc, processed/parsed, then inserted into the outputAS (output
# * annotation set).
# * /
# JapeRhsProcessor processor = new JapeRhsProcessor("echocardiogram", var_name, doc, bindings, outputAS);
# }
