from gatenlp.pam.pampac import actions, Getter
from gatenlp.pam.pampac import GetFeature


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
