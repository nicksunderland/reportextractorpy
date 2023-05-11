from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase, FeatureMatcher
from typing import List
import re


class AortaDiameter(AbstractPatternAnnotator):

    def __init__(self, outset_name):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented
        self.templates = [{"var_name": "ao_root_diam","descriptor": "aortic_root"},
                          {"var_name": "ao_sov",      "descriptor": "sinus_of_valsalva"},
                          {"var_name": "ao_stj_diam", "descriptor": "sinotubular_junction"},
                          {"var_name": "ao_asc_diam", "descriptor": "ascending_aorta"}]
        self.outset_name = outset_name
        self.included_annots = [("", ["Token", "Anatomy", "Numeric", "Units", "Lookup",
                                      "VarSentence", "Split", "Categorical", "BlockedContext"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []
        """
        Macro: CONTEXT
                    (
                {Anatomy,
                    Anatomy within {VarSentence.minorType == [descriptor]},
                    Anatomy notWithin {BlockedContext.type == [variable_name]},
                    Anatomy.minorType == [descriptor]}
                ({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string=="/"} | {Token.string==","})?
            )
        """
        context = \
            AnnAt(type="Units", features=FeatureMatcher(major="length"), name="units") \
            .notat(type="Units", features=FeatureMatcher(minor="mm"))
        # how to do this???    !Units.minorType == "mm"}

        act = AddAnn(type="test")
        rule_list.append(Rule(context, act))

        """
        Macro: CONTEXT_OTHER_AORTA
            (
                {Anatomy,
                    Anatomy within {VarSentence.minorType == [descriptor]},
                    Anatomy.majorType == "aorta", 
                    Anatomy.minorType != [descriptor]}
                ({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {Token.string=="/"} | {Token.string==","})?
            )
        """
        # context = \
        #     AnnAt(

        """
        Macro: CONTEXT_AORTA_ROOT
                (
                {Anatomy,
                 Anatomy within {VarSentence.minorType == [descriptor]},
                 Anatomy.majorType == "aorta",
                 Anatomy.minorType == "aortic_root"}
                ({Lookup.minorType == "conjunction"} | {Lookup.minorType == "preposition"} | {
                    Token.string == "/"} | {Token.string == ","})?
                )
        """

        """
        Macro: FILTER
            (
                {Token,
                    !Anatomy,
                    !Units.majorType == "length",
                    !Lookup.majorType == "quantity_change",
                    !Lookup.majorType == "height",
                    !Lookup.majorType == "body_surface_area",
                    !Lookup.majorType == "normal_range",
                    !Units.majorType == "z_score", 
                    Token within {VarSentence.minorType == [descriptor]}}
                | {Split}
            )
        """

        """
        Macro: VALUE
            (
                {Numeric, 
                    Numeric within {VarSentence.minorType == [descriptor]},
                    Numeric.type == "double"} |
                {Numeric,
                    Numeric within {VarSentence.minorType == [descriptor]}, 
                    Numeric.type == "integer"}
            )
        """

        """
        Macro: UNITS
            (
                {Units,
                    Units within {VarSentence.minorType == [descriptor]},
                    Units.majorType == "length"}
            )
        """

        """
        BlockIndexed
        Description: block things that start with indexed
        Example: 'indexed SoV 33mm.' 
        
        Rule: ao_idx_diam_blocker_1
        Priority: 100
        (	
            {Lookup.majorType == "indexed", 
                Lookup within {VarSentence.minorType == [descriptor]}}
            
            ( CONTEXT ):context
            
        ):indexed_diam_blocker
        -->
        :indexed_diam_blocker.Blocked = {type = [variable_name], rule = "ao_idx_diam_blocker_1"},
        :context.BlockedContext = {type = [variable_name], rule = "ao_idx_diam_blocker_1"}
        """

        """
        Aorta diameter rule 1
        Description: the most common form
        Example: 
            'the Stj is dilated at 45mm'
            'the `Stj and Sov are 3.0cm'

        Rule: ao_diam_1
        Priority: 100
        (
            (	
                 ((CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
                 ((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
                 ((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1]))
            ):context	
            
            ( FILTER )[0,15]
        
            ( VALUE ):value
            
            ( (UNITS)? ):unit
                    
            ({Token, 
                !Anatomy.majorType == "misc_echo_descriptor",
                !Units} | {Split})
            
        ):annot
        --> 
        :annot.varName = {var_name = [variable_name]}, 
        """


        """
        Aorta diameter rule 2
        Description: the rule captures more complicated phrases of the form:
        Example: 
            "Aortic root measures 4,2cm at the level of the stj."
            "Aortic root measures 4,2cm at the level of the sov and stj."

        Rule: ao_diam_2
        Priority: 99
        (
            ( CONTEXT_AORTA_ROOT )
            
            ( FILTER )[0,5]
            
            ( VALUE ):value
                    
            ( (UNITS)? ):unit
        
            {Lookup.minorType == "preposition"}
            
            ( FILTER )[0,5]
                
            (	
                (CONTEXT (CONTEXT_OTHER_AORTA)[0,2]) |
                ((CONTEXT_OTHER_AORTA)[0,2] CONTEXT) |
                ((CONTEXT_OTHER_AORTA)[0,1] CONTEXT (CONTEXT_OTHER_AORTA)[0,1])
            ):context	
        
        ):annot 
        --> 
        :annot.varName = {var_name = [variable_name]}, 
        """


        """
        Aorta diameter rule 3
        Description: the rule captures things of the forms:
        Example: 
            "non-dilated aortic root (33mm Stj level)"
            "non-dilated aortic root (33mm Sov, 35mm Stj)"
            "non-dilated aortic root (35mm Stj, 33mm Sov)"
            "aortic root non dilated (3.5cm stj)"
            "Non dilated proximal aorta (3.5cm stj)"
            "Non dilated proximal aorta (3.1cm at the STJ, 3.1cm at the SOV, 3.1cm at the Asc Ao level)"

         Rule: ao_diam_3
        Priority: 98
        (
                        
            ( CONTEXT_AORTA_ROOT )
            
            ({Categorical})[0,2]
                    
            {Token.kind == "punctuation", Token.position == "startpunct"}
            
            (
                ( VALUE )
                ( (UNITS)? )
                ( {Lookup.minorType == "preposition"} )[0,1]
                ( {Token} )[0,1]
                ( CONTEXT_OTHER_AORTA )
            )[0,2]
            
            
            ( VALUE ):value
            ( (UNITS)? ):unit
            ( {Lookup.minorType == "preposition"} )[0,1]
            ( {Token} )[0,1]
            ( CONTEXT ):context
            
        ):annot 
        --> 
        :annot.varName = {var_name = [variable_name]}, 
        """

        """
        Aorta diameter rule 4
        Description: The rule uses a more relaxed filter but enforces the units.
        Example: 
            "STJ within normal limits when indexed for BSA = 4.2cm (indexed 1.9cm/m2)"

          Rule: ao_diam_4
        Priority: 97
        (
            ( CONTEXT ):context
            
            ( {Token,
                !Anatomy.minorType != [descriptor],
                !Units.majorType == "length",
                !Lookup.majorType == "quantity_change",
                Token within {VarSentence.minorType == [descriptor]}} )[0,10]
            
            ( VALUE ):value
                    
            ( UNITS ):unit
            
            ({Token, 
                !Anatomy.majorType == "misc_echo_descriptor",
                !Units} | {Split})
        
        ):annot 
        --> 
        :annot.varName = {var_name = [variable_name]},
        """



        """
        Aorta diameter rule 5
        Description: The rule uses a more relaxed filter but enforces the units.
        Example: 
            "STJ within normal limits when indexed for BSA = 4.2cm (indexed 1.9cm/m2)"
        
          Rule: ao_diam_4
        Priority: 97
        (
            ( CONTEXT ):context
        
            ( {Token,
                !Anatomy.minorType != [descriptor],
                !Units.majorType == "length",
                !Lookup.majorType == "quantity_change",
                Token within {VarSentence.minorType == [descriptor]}} )[0,10]
        
            ( VALUE ):value
        
            ( UNITS ):unit
        
            ({Token, 
                !Anatomy.majorType == "misc_echo_descriptor",
                !Units} | {Split})
        
        ):annot 
        """

        return rule_list
