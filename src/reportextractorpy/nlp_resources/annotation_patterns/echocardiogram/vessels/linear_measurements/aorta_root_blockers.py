from reportextractorpy.abstract_pattern_annotator import AbstractPatternAnnotator
from reportextractorpy.custom_rule_actions import GetNumberFromNumeric
from gatenlp.pam.pampac import Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, RemoveAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase, FeatureMatcher
from typing import List
import re


class BlockingAorticRootDiameter(AbstractPatternAnnotator):

    def __init__(self, outset_name):
        self.var_name = NotImplemented
        self.descriptor = NotImplemented
        self.templates = [{"var_name": "ao_root_diam", "descriptor": "aortic_root"},
                          {"var_name": "ao_asc_diam", "descriptor": "ascending_aorta"},
                          {"var_name": "ao_root_diam_ht_idx", "descriptor": "aortic_root"},
                          {"var_name": "ao_asc_diam_ht_idx", "descriptor": "ascending_aorta"},
                          {"var_name": "ao_root_cat", "descriptor": "aortic_root"},
                          {"var_name": "ao_asc_cat", "descriptor": "ascending_aorta"}]
        self.outset_name = outset_name
        self.included_annots = [("", ["Token", "Anatomy", "Numeric", "Units", "Lookup",
                                      "VarSentence", "Split", "Categorical", "SectionHeader"])]
        self.pampac_skip = "longest"
        self.pampac_select = "first"
        self.rule_list = self.gen_rule_list()
        AbstractPatternAnnotator.__init__(self, **self.__dict__)

    def gen_rule_list(self) -> List[Rule]:
        rule_list = []
        """
        Aortic Root Blocker 1
        Description: Specific blockers go here, generic blockers can go in the base grammar file.
        Run this phase before either an 'aortic_root' phase, or an 'ascending_aorta'
        phase, as both of these descriptors commonly get used to refer to the aortic
        root in general. 
        Block general references to the proximal aorta followed by a more 
        specific reference to part of the proximal aorta BUT the value-context 
        is reversed such that the normal rules do not block it.
        Examples: 
            'aortic root non-dilated (33mm at Sov level)'
            'non-dilated aortic root (33mm Sov level)'
            'Mildly dilated proximal aorta (3.9cm at sinus level...'
        """
        blocker_pat_1 = (
            Seq(
                AnnAt(type="Categorical").repeat(0, 2),
                AnnAt(type="Token").repeat(0, 2)
            ).repeat(0, 2) >>

            AnnAt(type="Anatomy", features=FeatureMatcher(minor="aortic_root"), name="context")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Token").repeat(0, 1) >>

            AnnAt(type="Categorical").repeat(0, 2) >>

            AnnAt(type="Token", features=FeatureMatcher(kind="punctuation", position="startpunct")) >>

            AnnAt(type="Numeric").within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Units", features=FeatureMatcher(major="length"))
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
            .repeat(0, 1) >>

            AnnAt(type="Lookup", features=FeatureMatcher(minor="preposition")).repeat(0, 1) >>

            AnnAt(type="Token").repeat(0, 4) >>

            Or(
                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1),

                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinotubular_junction"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1)
            )
        )

        blocker_act_1a = AddAnn(type="BlockedPhrase",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_1"})
        blocker_act_1b = AddAnn(type="BlockedContext",
                                name="context",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_1"})
        rule_list.append(Rule(blocker_pat_1, blocker_act_1a, blocker_act_1b))

        """
        Aortic Root Blocker 2
        Description: Block general references to the proximal aorta followed by a more
        specific reference to part of the proximal aorta BUT the value-context
        is reversed such that the normal rules do not block it.
        Examples: 
            'The proximal aorta is dilated at 4.7cm (sinus level)'
        """
        blocker_pat_2 = (
            Seq(
                AnnAt(type="Categorical").repeat(0, 2),
                AnnAt(type="Token").repeat(0, 2)
            ).repeat(0, 2) >>

            AnnAt(type="Anatomy", features=FeatureMatcher(minor="aortic_root"), name="context")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Token").repeat(0, 1) >>

            AnnAt(type="Categorical").repeat(0, 2) >>

            AnnAt(type="Token").repeat(0, 5) >>

            AnnAt(type="Token", features=FeatureMatcher(kind="punctuation", position="startpunct")) >>

            AnnAt(type="Token").repeat(0, 5) >>

            Or(
                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1),

                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinotubular_junction"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1)
            )
        )

        blocker_act_2a = AddAnn(type="BlockedPhrase",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_2"})
        blocker_act_2b = AddAnn(type="BlockedContext",
                                name="context",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_2"})
        rule_list.append(Rule(blocker_pat_2, blocker_act_2a, blocker_act_2b))

        """
        Aortic Root Blocker 3
        Description: Specific blockers go here, generic blockers can go in the base grammar file.
        Block general references to the proximal aorta followed by a more
        specific reference to part of the proximal aorta.
        Examples: 
            'Aortic root 4.2cm at sinus of valsalva'
            'Aortic root not dilated 4,2cm at the level of the sinuses'
            'Aortic root measures 4,2cm at the level of the sinuses'
            'Non dilated proximal aorta to sinus level.'
            'Non-dilated aortic root at the Sov and Stj'
            'no significant dilatation of the aortic root at sinus level'
            'Normal aortic root with a dilated asc ao (4.1cm).''
        """
        blocker_pat_3 = (
            Seq(
                AnnAt(type="Categorical").repeat(0, 2),
                AnnAt(type="Token").repeat(0, 2)
            ).repeat(0, 2) >>

            AnnAt(type="Anatomy", features=FeatureMatcher(minor="aortic_root"), name="context")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Token")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
            .notat(type="Anatomy", features=FeatureMatcher(minor="aortic_root"))
            .notat(type="Categorical")
            .repeat(0, 10) >>

            AnnAt(type="Lookup", features=FeatureMatcher(minor="preposition")) >>

            AnnAt(type="Token").repeat(0, 4) >>

            Or(
                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1),

                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinotubular_junction"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1)
            )
        )

        blocker_act_3a = AddAnn(type="BlockedPhrase",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_3"})
        blocker_act_3b = AddAnn(type="BlockedContext",
                                name="context",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_3"})
        rule_list.append(Rule(blocker_pat_3, blocker_act_3a, blocker_act_3b))

        """
        Aortic Root Blocker 4
        Description: Specific blockers go here, generic blockers can go in the base grammar file.
        Block general references to the proximal aorta followed by a more specific reference to 
        part of the proximal aorta.
        Examples: 
            'Normal calibre proximal aortic root, sinus of Valsalva = 2.9cm.'
        """
        blocker_pat_4 = (
            Seq(
                AnnAt(type="Categorical").repeat(0, 2),
                AnnAt(type="Token").repeat(0, 2)
            ).repeat(0, 2) >>

            AnnAt(type="Anatomy", features=FeatureMatcher(minor="aortic_root"), name="context")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Token")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
            .notat(type="Anatomy", features=IfNot(FeatureMatcher(minor=self.descriptor)))
            .notat(type="Categorical")
            .repeat(0, 10) >>

            AnnAt(type="Token").repeat(0, 4) >>

            Or(
                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinus_of_valsalva"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1),

                AnnAt(type="Anatomy", features=FeatureMatcher(minor="sinotubular_junction"))
                .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
                .repeat(0, 1)
            ) >>

            AnnAt(type="Token").repeat(0, 4) >>

            AnnAt(type="Numeric").within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Units", features=FeatureMatcher(major="length"))
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
            .repeat(0, 1)
        )

        blocker_act_4a = AddAnn(type="BlockedPhrase",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_4"})
        blocker_act_4b = AddAnn(type="BlockedContext",
                                name="context",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_4"})
        rule_list.append(Rule(blocker_pat_4, blocker_act_4a, blocker_act_4b))

        """
        Aortic Root Blocker 5
        Description: Specific blockers go here, generic blockers can go in the base grammar file.
        Block general references to the proximal aorta followed by a more
        specific reference to part of the proximal aorta. We don't allow ascending aorta to
        escape this block as the root reference is just a section header.
        Examples: 
            'HAMB_AO_ASC_TEXT: Proximal ascending aorta 55cm. This is not dilated indexed to BSA.
            Aortic root at SoV measures 44cm, this is dilated.'
        """
        blocker_pat_5 = (
            Seq(
                AnnAt(type="Categorical").repeat(0, 2),
                AnnAt(type="Token").repeat(0, 2)
            ).repeat(0, 2) >>

            AnnAt(type="Anatomy", features=FeatureMatcher(minor="aortic_root"), name="context")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
            .within(type="SectionHeader", features=FeatureMatcher(minor="aorta")) >>

            AnnAt(type="Token")
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
            .notat(type="Anatomy", features=IfNot(FeatureMatcher(minor=self.descriptor)))
            .notat(type="Categorical")
            .repeat(0, 10) >>

            AnnAt(type="Token").repeat(0, 4) >>

            AnnAt(type="Anatomy", features=FeatureMatcher(major="aorta"))
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Token").repeat(0, 1) >>

            AnnAt(type="Numeric").within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor)) >>

            AnnAt(type="Units", features=FeatureMatcher(major="length"))
            .within(type="VarSentence", features=FeatureMatcher(minor=self.descriptor))
            .repeat(0, 1)
        )

        blocker_act_5a = AddAnn(type="BlockedPhrase",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_5"})
        blocker_act_5b = AddAnn(type="BlockedContext",
                                name="context",
                                annset_name="",
                                features={"type": self.var_name, "rule": "ao_root_blocker_5"})
        rule_list.append(Rule(blocker_pat_5, blocker_act_5a, blocker_act_5b))

        return rule_list
