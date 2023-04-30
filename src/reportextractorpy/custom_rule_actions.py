from gatenlp.pam.pampac import actions, Getter
from gatenlp.pam.pampac import GetFeature
from typing import List


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


class GetList(Getter):
    """
    Helper to return a list of matches which may come from multiple named capture groups.
    """
    def __init__(self,
                 name=None,
                 silent_fail=False):
        assert name is not None
        self.name = name
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):

        text_to_return = []

        for i, r in enumerate(succ._results):
            for match in r.matches4name(self.name):
                span = match.get("span")
                text = context.doc[span]
                text_to_return.append(text)

        if not text_to_return:
            if self.silent_fail:
                return []
            else:
                raise Exception(
                    f"Could not find annotations of name: {self.name}"
                )

        return text_to_return


class RemoveAnnAll:
    """
    Action for removing annotations.
    """

    def __init__(self,
                 name: str | List[str] = None,
                 type: str | List[str] = None,
                 annset_name: str = None,
                 silent_fail: bool = True):
        """
        Create a remove all annotation action.
        Args:
            name: the name, or list of names, of a match(es) from which to get the annotation to remove
            type: the annotation type, or list of types, of annotation within the whole matched pattern to
                remove, if the name parameter is supplied then only named elements of these types will be
                removed. If no name or type is provided all annotations in the span will be removed.
            annset_name: the name of the annotation set to remove the annotation from. If this is the same set
                as used for matching it may influence the matching result if the annotation is removed before
                the remaining matching is done.
                If this is not specified, the annotation set of the (first) input annotation is used.
            silent_fail: if True, silently ignore the error of no annotation to get removed
        """
        assert any([name, type]), \
            f"either name and/or type should be provided [name: {name}, type: {type}]"

        if name is not None:
            assert all(isinstance(c, str) for c in name), \
                f"name must be a string or list of strings but is {name}"
            if isinstance(name, list):
                self.name = name
            else:
                self.name = [name]
        else:
            self.name = None

        if type is not None:
            assert all(isinstance(c, str) for c in type), \
                f"type must be a string or list of strings but is {type}"
            if isinstance(type, list):
                self.type = type
            else:
                self.type = [type]
        else:
            self.type = None

        assert annset_name is None or isinstance(annset_name, str), \
            f"annset_name must be a string or None but is {annset_name}"
        self.annset_name = annset_name
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None, annset=None):

        if len(succ) == 0:
            if not self.silent_fail:
                raise Exception(f"No results: {succ}")
            return None

        if self.annset_name is not None:
            annset = context.doc.annset(self.annset_name)

        for res in succ:

            # all annotations in pattern match span
            anns_all = annset.within(res.span.start, res.span.end)
            if self.type is not None:
                if not any([t in self.type for t in anns_all.type_names]):
                    if self.silent_fail:
                        return
                    else:
                        raise Exception(
                            f"Could not find any annotation type for the type(s) {self.type}"
                        )

            # name(s) provided - look for annotations
            anns_named = set()
            if self.name is not None:
                for name in self.name:
                    for match in res.matches4name(name):
                        ann = match.get("ann")
                        if ann is not None:
                            anns_named.add(ann)

                if not anns_named:
                    if self.silent_fail:
                        return
                    else:
                        raise Exception(
                            f"Could not find any annotation for the name(s) {self.name}"
                        )

            # Handle each annotation in turn
            for ann in anns_all:
                # no name and no type specified - removal all annotations
                if self.name is None and self.type is None:
                    annset.remove(ann)
                # both name and type specified - removal all named annotations of those types
                elif self.name is not None and self.type is not None:
                    if ann in anns_named and ann.type in self.type:
                        annset.remove(ann)
                # only name specified - remove named annotations
                elif self.name is not None and self.type is None:
                    if ann in anns_named:
                        annset.remove(ann)
                # only type specified - remove annotations of that type
                elif self.name is None and self.type is not None:
                    if ann.type in self.type:
                        annset.remove(ann)
                # shouldn't get here
                else:
                    raise Exception("RemoveAnnAll() code error")
