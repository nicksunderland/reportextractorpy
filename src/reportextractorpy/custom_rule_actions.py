from gatenlp.pam.pampac import actions, Getter
from gatenlp.pam.pampac.actions import _get_span, _get_match
import inspect


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


# Wont need these when the fix is implemented in GATE
"""
Module for PAMPAC getter helper classes
"""
class GetAnn(Getter):
    """
    Helper to access an annoation from a match with the given name.
    """

    def __init__(self, name, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetAnn helper.
        Args:
            name: the name of the match to use.
            resultidx:  the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None.
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):

        match = _get_match(
            succ, self.name, self.resultidx, self.matchidx, self.silent_fail
        )

        try:
            ann = match.get("ann")
        except AttributeError:
            ann = None

        if ann is None:
            if not self.silent_fail:
                raise Exception(
                    f"No annotation found for name {self.name}, {self.resultidx}, {self.matchidx}"
                )
        return ann


class GetFeatures(Getter):
    """
    Helper to access the features of an annotation in a match with the given name.
    """

    def __init__(self, name, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetFeatures helper.
        Args:
            name: the name of the match to use.
            resultidx: the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        match = _get_match(
            succ, self.name, self.resultidx, self.matchidx, self.silent_fail
        )
        try:
            ann = match.get("ann")
        except AttributeError:
            ann = None
        if ann is None:
            if not self.silent_fail:
                raise Exception(
                    f"No annotation found for name {self.name}, {self.resultidx}, {self.matchidx}"
                )
        return ann.features


class GetType(Getter):
    """
    Helper to access the type of an annotation in a match with the given name.
    """

    def __init__(self, name, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetType helper.
        Args:
            name: the name of the match to use.
            resultidx: the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        match = _get_match(
            succ, self.name, self.resultidx, self.matchidx, self.silent_fail
        )
        try:
            ann = match.get("ann")
        except AttributeError:
            ann = None
        if ann is None:
            if not self.silent_fail:
                raise Exception(
                    f"No annotation found for name {self.name}, {self.resultidx}, {self.matchidx}"
                )
        return ann.type


class GetStart(Getter):
    """
    Helper to access the start offset of the annotation in a match with the given name.
    """

    def __init__(self, name, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetStart helper.
        Args:
            name: the name of the match to use.
            resultidx: the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        match = _get_match(
            succ, self.name, self.resultidx, self.matchidx, self.silent_fail
        )
        try:
            span = match["span"]
        except TypeError:
            span = None

        if span is None:
            if not self.silent_fail:
                raise Exception(
                    f"No annotation found for name {self.name}, {self.resultidx}, {self.matchidx}"
                )

        return span.start


class GetEnd(Getter):
    """
    Helper to access the end offset of the annotation in a match with the given name.
    """

    def __init__(self, name, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetEnd helper.
        Args:
            name: the name of the match to use.
            resultidx: the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        return _get_match(
            succ, self.name, self.resultidx, self.matchidx, self.silent_fail
        )["span"].end


class GetFeature(Getter):
    """
    Helper to access the features of the annotation in a match with the given name.
    """

    def __init__(self, name, featurename, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetFeatures helper.
        Args:
            name: the name of the match to use.
            resultidx: the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail
        self.featurename = featurename

    def __call__(self, succ, context=None, location=None):
        match = _get_match(
            succ, self.name, self.resultidx, self.matchidx, self.silent_fail
        )
        try:
            ann = match.get("ann")
        except AttributeError:
            ann = None
        if ann is None:
            if not self.silent_fail:
                raise Exception(
                    f"No annotation found for name {self.name}, {self.resultidx}, {self.matchidx}"
                )
        return ann.features.get(self.featurename)


class GetText(Getter):
    """
    Helper to access text, either covered document text of the annotation or matched text.
    """

    def __init__(self, name=None, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetText helper. This first gets the span that matches the name, resultidx and matchidx
        parameters and then provides the text of the document for that span.
        Args:
            name: the name of the match to use, if None, use the span of the whole match.
            resultidx: the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        if self.name is None:
            span = _get_span(succ, self.name, self.resultidx, self.matchidx, self.silent_fail)
        else:
            match = _get_match(
                succ, self.name, self.resultidx, self.matchidx, self.silent_fail
            )
            try:
                span = match.get("span")
            except AttributeError:
                span = None

        if span:
            return context.doc[span]
        else:
            if self.silent_fail:
                return None
            else:
                raise Exception("Could not find a span for match info")


class GetRegexGroup(Getter):
    """
    Helper to access the given regular expression matching group in a match with the given name.
    """

    def __init__(self, name, group=0, resultidx=0, matchidx=0, silent_fail=False):
        """
        Create a GetText helper.
        Args:
            name: the name of the match to use.
            resultidx: the index of the result to use if there is more than one.
            matchidx:  the index of the match info element with the given name to use if there is more than one
            silent_fail: if True, do not raise an exception if the annotation cannot be found, instead return
                None
        """
        self.name = name
        self.resultidx = resultidx
        self.matchidx = matchidx
        self.group = group
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None):
        match = _get_match(
            succ, self.name, self.resultidx, self.matchidx, self.silent_fail
        )
        try:
            groups = match.get("groups")
        except AttributeError:
            groups = None

        if groups:
            return groups[self.group]
        else:
            if self.silent_fail:
                return None
            else:
                raise Exception("Could not find regexp groups for match info")


class ParseNumericUnits(Getter):
    """
    Helper to parse value:units annotation groups.
    """
    std_length = "cm"
    std_velocity = "m/s"
    std_mass = "kg"
    std_pressure = "cmH2O"
    unit_map = {
        # Length units
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'km': 1000.0,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.34,
        # Weight units
        'mg': 0.000001,
        'g': 0.001,
        'kg': 1.0,
        'lb': 0.453592,
        'oz': 0.0283495,
        'st': 6.35029,  # stone
        # Pressure units
        'Pa': 1.0,
        'kPa': 1000.0,
        'MPa': 1000000.0,
        'psi': 6894.76,
        'bar': 100000.0,
        'cmH2O': 98.0665,  # centimeters of water column
        # Velocity units
        'm/s': 1.0,
        'km/h': 0.277778,
        'mph': 0.44704
    }

    def __init__(self,
                 name_value: str,
                 name_units: str | None,
                 func: callable = lambda x: sum([float(v) for v in x]) / len(x),
                 var_type: str = None,
                 silent_fail: bool = False):
        """
        Create a ParseNumericUnits helper.
        Args:
            name_value: the name of the value match to use.
            name_units: the name of the units match to use.
            func: the function to apply if 2 values are matched
            silent_fail: if True, do not raise an exception if annotations cannot be found, instead return None
        :return a dictionary {value: XX, units: YY}
        """
        self.name_value = name_value
        self.name_units = name_units
        self.func = func
        self.var_type = var_type
        self.silent_fail = silent_fail

    def __call__(self, succ, context=None, location=None) -> dict:

        text, value, units, tups, parse_info = None, None, None, None, None

        try:
            result = succ[0]
            text_span = result.span
            text = context.doc[text_span]
        except IndexError as e:
            raise Exception(f"{e}, no results in Success object {succ} when firing ParseNumericUnits()")

        try:
            value_matches = [float(match.get("ann").features["value"]) for match in result.matches
                             if match.get("name") == self.name_value and match.get("ann").type == "Numeric"]

            unit_matches = [match.get("ann").features["minor"] for match in result.matches
                            if match.get("name") == self.name_units and match.get("ann").type == "Units"]

            #print(value_matches)

            if not value_matches:
                imp_anns = [match.get("ann") for match in result.matches
                            if match.get("name") == self.name_value and match.get("ann").type == "ImperialMeasurement"]

                #print(imp_anns)

                if imp_anns:
                    ann = imp_anns[0]
                    self.func = lambda x: sum(x)
                    if ann.features["major"] == "mass":
                        value_matches = [ann.features["stone"], ann.features["pounds"]]
                        unit_matches = ["st", "lb"]
                    elif ann.features["major"] == "length":
                        value_matches = [ann.features["feet"], ann.features["inches"]]
                        unit_matches = ["ft", "in"]
                    else:
                        value_matches = []
                        unit_matches = []

            if len(value_matches) == 0:
                raise Exception(f"No values parsed from matches:\n{result.matches}")

            if len(unit_matches) == len(value_matches):
                tups = [t for t in zip(value_matches, unit_matches) if t[0] is not None]
            elif len(unit_matches) == 1 and len(value_matches) > 1:
                tups = [t for t in zip(value_matches, unit_matches * len(value_matches)) if t[0] is not None]
            else:
                # TODO function to guess units from config file
                tups = [t for t in zip(value_matches, [""] * len(value_matches)) if t[0] is not None]
                pass

            #print(tups)

            normalised_values, normalised_units = zip(*self.standardize_units(tups))
            if len(normalised_values) > 1:
                value = self.func(normalised_values)
                units = normalised_units[0]
                parse_info = f'{inspect.getsource(self.func)}'
            else:
                value = normalised_values[0]
                units = normalised_units[0]
                parse_info = f'Normalised value from {tups[0][1]} to {normalised_units[0]}'

        except Exception as e:
            print("excepted")

        return {"context": text, "value": round(value, 2), "units": units, "parse_info": parse_info}

    @classmethod
    def convert(cls, value, from_unit, to_unit):
        """
        Converts a value from one unit to another.

        Parameters:
            value (float): The value to convert.
            from_unit (str): The unit to convert from.
            to_unit (str): The unit to convert to. Defaults to 'm'.

        Returns:
            float: The converted value in the specified unit.
        """
        if from_unit not in cls.unit_map:
            raise ValueError(f"Unknown unit: {from_unit}")
        if to_unit not in cls.unit_map:
            raise ValueError(f"Unknown unit: {to_unit}")
        return value * cls.unit_map[from_unit] / cls.unit_map[to_unit]

    @classmethod
    def standardize_units(cls, input_list):
        """
        Converts a list of tuples containing a float and a string representing the unit to SI units.

        Parameters:
            input_list (list): A list of tuples containing a float and a string representing the unit.

        Returns:
            list: A list of tuples with the float standardised to SI units and the string representing
                  the units it has been standardised to.
        """
        output_list = []
        for value, unit in input_list:

            try:
                if unit in ['mm', 'cm', 'm', 'km', 'in', 'ft', 'yd', 'mi']:
                    # Convert length
                    standard_value = cls.convert(value, unit, cls.std_length)
                    output_list.append((standard_value, cls.std_length))
                elif unit in ['mg', 'g', 'kg', 'lb', 'oz', 'st']:
                    # Convert mass
                    standard_value = cls.convert(value, unit, cls.std_mass)
                    output_list.append((standard_value, cls.std_mass))
                elif unit in ['Pa', 'kPa', 'MPa', 'psi', 'bar', 'cmH2O']:
                    # Convert pressure
                    standard_value = cls.convert(value, unit, cls.std_pressure)
                    output_list.append((standard_value, cls.std_pressure))
                elif unit in ['m/s', 'km/h', 'mph']:
                    # Convert velocity
                    standard_value = cls.convert(value, unit, cls.std_velocity)
                    output_list.append((standard_value, cls.std_velocity))
                else:
                    output_list.append((value, unit))

            except ValueError:
                output_list.append((value, unit))

        return output_list
