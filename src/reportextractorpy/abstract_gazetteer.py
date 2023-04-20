from abc import ABC
from typing import List


class AbstractGazetteer(ABC):
    # The annotation type, e.g. "Anatomy"
    annot_type: str = NotImplemented

    # The annotation features, e.g. {"major": "aorta", "minor": "ascending_aorta"}
    annot_features: dict = NotImplemented

    # A list of strings to match in the document e.g. ["aorta", "ao"]
    # input these as all lowercase, any mixed case strings should go in the regex rules
    string_matches: List[str] = NotImplemented

    # A list of regex rules to match in the document e.g.
    # rules1 = """
    # |[0-9]{4}-[0-9]{2}-[0-9]{2}
    # 0 => Date
    # """
    # see: https://gatenlp.github.io/python-gatenlp/stringregex
    regex_rules: str = NotImplemented
