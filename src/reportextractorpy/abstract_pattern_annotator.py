from abc import ABC, abstractmethod
from typing import List, Tuple

import gatenlp
from gatenlp.pam.pampac import PampacAnnotator, Pampac, Rule, Result, actions, Getter, PampacParser, Success, Failure
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures, RemoveAnn
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase


class AbstractPatternAnnotator(PampacAnnotator, ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        self.annotator_outset_name = NotImplementedError
        self.rule_list = [NotImplementedError]
        self.var_name = NotImplementedError
        self.included_annots = NotImplementedError
        self.pampac_skip = NotImplementedError
        self.pampac_select = NotImplementedError
        for k, v in kwargs.items():
            if k in self.__dict__:
                setattr(self, k, v)
            # else:  need to allow other variables in the derived class???
            #     raise KeyError(k)
        pampac = Pampac(*self.rule_list, skip=self.pampac_skip, select=self.pampac_select)
        PampacAnnotator.__init__(self,
                                 pampac,
                                 annspec=self.included_annots,
                                 outset_name=self.annotator_outset_name)

    @abstractmethod
    def gen_rule_list(self) -> List[Rule]:
        pass

    def validator(self):
        # TODO: create this self.validator() function
        print("validating some stuff e.g.: " + str(self.pampac_select))
        #
        # for rule in self._rule_list:
        #     print(rule.parser.parsers)

        # make sure that the annotations referred to in the rules all exist in _included_annots
        # assert all([hasattr(self, "_annotator_outset_name"),
        #             hasattr(self, "_var_name"),
        #             hasattr(self, "_included_annots"),
        #             hasattr(self, "_pampac_skip"),
        #             hasattr(self, "_pampac_select"),
        #             hasattr(self, "_rule_list")])

    @staticmethod
    def sub_match_result(result: Result, name: str) -> str | dict:
        try:
            if len(result.matches4name(name)) == 1:
                return result.matches4name(name)[0]
            elif len(result.matches4name(name)) > 1:
                raise IndexError
            else:
                return {}
        except IndexError:
            print("AbstractPatternAnnotator.sub_match_result() returned multiple sub-pattern matches."
                  "Check the annotation pattern doesn't contain duplicate sub-match naming")


class RemAnn:
    """
    Action for removing an annotation.
    """
    def __init__(self, name=None, annset_name="", resultidx=0, matchidx=0, silent_fail=True):
        assert name is not None
        self.name = name
        self.annset_name = annset_name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        annset = context.doc.annset(self.annset_name)
        match = actions._get_match(succ, self.name, self.resultidx, self.matchidx, self.silent_fail)
        if not match:
            if self.silent_fail:
                return
            else:
                raise Exception(f"Could not find the name {self.name}")
        theann = match.get("ann")
        if theann is None:
            if self.silent_fail:
                return
            else:
                raise Exception(
                    f"Could not find an annotation for the name {self.name}"
                )
        annset.remove(theann.id)


class GetNumberFromText(Getter):
    """
    Helper to average two numerical annotations.
    """
    def __init__(self,
                 name_1=None,
                 name_2=None,
                 func: callable = lambda x, y: (float(x) + float(y))*0.5,
                 resultidx=0,
                 matchidx=0,
                 silent_fail=False):
        self.name_1 = name_1
        self.name_2 = name_2
        self.func = func
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):

        span_1, span_2 = None, None

        # No group names provided
        if not any([self.name_1, self.name_2]):
            span_1 = actions._get_span(succ, self.name_1, self.resultidx, self.matchidx, self.silent_fail)
            span_2 = actions._get_span(succ, self.name_2, self.resultidx, self.matchidx, self.silent_fail)

        # Single value group provided
        elif any([self.name_1, self.name_2]) and not all([self.name_1, self.name_2]):

            if self.name_1 is not None:
                match = actions._get_match(succ, self.name_1, self.resultidx, self.matchidx, self.silent_fail)
                span_1 = match.get("span")
            else:
                match = actions._get_match(succ, self.name_2, self.resultidx, self.matchidx, self.silent_fail)
                span_2 = match.get("span")

        # Both value groups provided
        elif all([self.name_1, self.name_2]):
            match_1 = actions._get_match(succ, self.name_1, self.resultidx, self.matchidx, self.silent_fail)
            match_2 = actions._get_match(succ, self.name_2, self.resultidx, self.matchidx, self.silent_fail)
            span_1 = match_1.get("span")
            span_2 = match_2.get("span")

        # shouldn't get here
        else:
            Exception("GetNumber(Getter) name parameter problem")

        try:
            if span_1 and span_2:
                number = float(self.func(context.doc[span_1], context.doc[span_2]))
            elif span_1:
                number = float(context.doc[span_1])
            elif span_2:
                number = float(context.doc[span_2])
            else:
                raise IndexError("Could not find a span for match info")
            return number

        except (ValueError, IndexError) as e:
            if self.silent_fail:
                return str(e)
            else:
                return None


class GetNumberFromNumeric(Getter):
    """
    Helper to average two numerical annotations.
    """
    def __init__(self,
                 name_1=None,
                 name_2=None,
                 func: callable = lambda x, y: (float(x) + float(y)) * 0.5,
                 silent_fail=False):
        assert any([name_1, name_2])
        self.name_1 = name_1
        self.name_2 = name_2
        self.func = func
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        try:
            # Single value group provided
            if any([self.name_1, self.name_2]) and not all([self.name_1, self.name_2]):
                if self.name_1 is not None:
                    return float(GetFeature(name=self.name_1,
                                            featurename="value",
                                            silent_fail=self.silent_fail).__call__(succ, context, location))
                else:
                    return float(GetFeature(name=self.name_2,
                                            featurename="value",
                                            silent_fail=self.silent_fail).__call__(succ, context, location))

            # Both value groups provided
            elif all([self.name_1, self.name_2]):
                v1 = float(GetFeature(name=self.name_1,
                                      featurename="value",
                                      silent_fail=self.silent_fail).__call__(succ, context, location))
                v2 = float(GetFeature(name=self.name_2,
                                      featurename="value",
                                      silent_fail=self.silent_fail).__call__(succ, context, location))
                return float(self.func(v1, v2))

            # shouldn't get here
            else:
                Exception("GetNumber(Getter) name parameter problem")

        except (ValueError, AttributeError) as e:
            if self.silent_fail:
                return None


class CustomLookahead(PampacParser):
    """
    Copy of GATEs to fix minor bug, hopefully theyll fix it in the main repository
    """

    def __init__(self, parser, laparser, matchtype="first"):
        """
        Create a Lookahead parser.

        Args:
            parser: the parser for which to return a success or failure
            laparser:  the parser that must match after the first parser, but it's success is discarded.
            matchtype: which matches to include in the result, one of "first", "longest", "shortest", "all".
        """
        self.parser = parser
        self.laparser = laparser
        self.matchtype = matchtype

    def parse(self, location, context):
        ret = self.parser.parse(location, context)  #.issuccess() <- this bug
        if ret.issuccess():
            res = ret.result(self.matchtype)
            if isinstance(res, list):
                # we need to check each of the results
                allres = []
                for mtch_ in res:
                    newlocation = mtch_.location
                    laret = self.laparser.parse(newlocation, context)
                    if laret.issuccess():
                        allres = []
                if len(allres) > 0:
                    return Success(results=allres, context=context)
                else:
                    return Failure(
                        context=context,
                        message="Lookahead failed for all results",
                        location=location,
                    )
            else:
                newlocation = res.location
                laret = self.laparser.parse(newlocation, context)
                if laret.issuccess():
                    return ret
                else:
                    return Failure(
                        context=context, message="Lookahead failed", location=location
                    )
        else:
            return ret

