import regex
import re
from abc import ABC
from typing import List, Tuple


class AbstractGazetteer(ABC):
    # The annotation type, e.g. "Anatomy"
    annot_type: str = NotImplemented

    # The annotation features, e.g. {"major": "aorta", "minor": "ascending_aorta"}
    annot_features: dict[str: str, str: str] = NotImplemented

    # A list of regex rules to match in the document - as re.Pattern or regex.Pattern objects
    # note heavy use of word boundaries, especially with short patterns or
    # obvious sub-components of longer words. e.g.
    # regex_rules = [
    #     regex.compile(r'(?<=\d)|(?<=\b)cms?\b', flags=regex.I),
    #     re.compile(r'centimet[re]{2}s?', flags=regex.I),
    # ]
    regex_rules: List[re.Pattern | regex.Pattern | Tuple[regex.Pattern | re.Pattern, str, dict]] = NotImplemented

    # Auto formatted regex with the annotation type and features
    # Example input / AbstractGazetteer derived class configuration:
    #   annot_type = "Date"
    #   annot_features = {"major": "example", "minor": "example"}
    #   regex_rules = [
    #       re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', flags=0),
    #       (re.compile(r'dog123', flags=0), "Animal", {"type": "dog"})
    #   ]
    # Example output (https://gatenlp.github.io/python-gatenlp/stringregex):
    # """
    #   |[0-9]{4}-[0-9]{2}-[0-9]{2}
    #   0 => Date   major="example", minor="example"
    #   |dog123
    #   0 => Animal   type="dog"
    # """
    # see: https://gatenlp.github.io/python-gatenlp/stringregex
    def formatted_regex_rules(self):
        try:
            comb_regex = ""
            for rule in self.regex_rules:
                if isinstance(rule, tuple) and (isinstance(rule[0], regex.Pattern) or isinstance(rule[0], re.Pattern)):
                    pattern = rule[0]
                    annot_type = rule[1]
                    annot_features = rule[2]
                elif isinstance(rule, regex.Pattern) or isinstance(rule, re.Pattern):
                    pattern = rule
                    annot_type = self.annot_type
                    annot_features = self.annot_features
                else:
                    raise TypeError(rule)

                # to extract the strings from the regex capture groups
                # set a fature to "assign_to_group_X", where X is the
                # group e.g. {"value": "assign_to_group_1"}, G1=group1
                # of the regex
                comb_regex = comb_regex + \
                             "|" + pattern.pattern + "\n" + \
                             "0 => " + annot_type + "  " + \
                             ", ".join([k + "=G" + v.lstrip("assign_to_group_")
                                        if "assign_to_group_" in v
                                        else k + "=\"" + v + "\""
                                        for k, v in annot_features.items()]) + \
                             "\n"
            return comb_regex

        except TypeError as e:
            print("Error parsing regular expression rules:")
            print(e)
