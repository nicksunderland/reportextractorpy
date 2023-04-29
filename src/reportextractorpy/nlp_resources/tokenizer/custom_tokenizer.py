from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import regex
import re


class CustomTokenizer(AbstractGazetteer):
    def __init__(self):
        self.annot_type = "Token"
        self.annot_features = {"kind": "word"}
        self.regex_rules = [
            (regex.compile(r'((?:\p{L}(?:\p{Mn})*)(?:(?:\p{Ll}(?:\p{Mn})*)|\p{Pd}|\p{Cf})*)', flags=regex.I), "Token", {"text": "assign_to_group_1"}),
            (re.compile(r'(?<!\d)(19|20\d\d)([- \/.])(0?[1-9]|1[012])\2(0?[1-9]|[12][0-9]|3[01])(?!\d)'), "Date", {"year": "assign_to_group_1", "month": "assign_to_group_3", "day": "assign_to_group_4"}),
            (re.compile(r'(?<!\d)(0?[1-9]|[12][0-9]|3[01])([- \/.])(0?[1-9]|1[012])\2(19|20\d\d)(?!\d)'), "Date", {"year": "assign_to_group_4", "month": "assign_to_group_3", "day": "assign_to_group_1"}),
            (re.compile(r'(?<!\d)(0[1-9]|[12][0-9]|3[01])[- \/.](0[1-9]|1[012])(?!\d)'), "Date", {"month": "assign_to_group_2", "day": "assign_to_group_1"}),
            (re.compile(r'(?<!\d)(0?[1-9]|1[012])[- \/.](19|20\d\d)(?!\d)'), "Date", {"year": "assign_to_group_2", "month": "assign_to_group_1"}),
            (re.compile(r'(?<!\d)(19|20\d\d)(?!\d)'), "Date", {"year": "assign_to_group_1"}),
            (re.compile(r'(?<!\d)([1234]?\d)\s?\/\s?52'), "Numeric", {"kind": "weeks", "value": "assign_to_group_1"}),
            (re.compile(r'(?<!\d)([1234]?\d)(?:\+[1-7])?\s?\/\s?40'), "Numeric", {"kind": "weeks", "value": "assign_to_group_1"}),
            (re.compile(r'((?:[0-9]*[.])?[0-9]+(?:[eE^][-+]?[0-9]+)?)'), "Numeric", {"value": "assign_to_group_1", "kind": "raw_text"}),
            (regex.compile(r'(?:\p{Zs})'), "SpaceToken", {"kind": "space"}),
            (regex.compile(r'(?:\p{Cc})'), "SpaceToken", {"kind": "control"}),
            (regex.compile(r'(\p{Sk}|\p{Sm}|\p{So})'), "Token", {"text": "assign_to_group_1", "kind": "symbol"}),
            (regex.compile(r'(\p{Sk}|\p{Sm}|\p{So})'), "Token", {"text": "assign_to_group_1", "kind": "symbol", "symbolkind": "currency"}),
            (regex.compile(r'(\p{Pd}|\p{Cf})'), "Token", {"text": "assign_to_group_1", "kind": "punctuation", "subkind": "dashpunct"}),
            (regex.compile(r'(\p{Pc}|\p{Po})'), "Token", {"text": "assign_to_group_1", "kind": "punctuation"}),
            (regex.compile(r'(\p{Ps}|\p{Pi})'), "Token", {"text": "assign_to_group_1", "kind": "punctuation", "position": "startpunct"}),
            (regex.compile(r'(\p{Pe}|\p{Pf})'), "Token", {"text": "assign_to_group_1", "kind": "punctuation", "position": "endpunct"}),
            (re.compile(r'(?:[.]{1,3}"?|[!?]{1,4})'), "Split", {"kind": "internal"}),
            (re.compile(r'\s*+\Z|'
                        r'(?:[\u00A0\u2007\u202F\s][^\n\r]|[^\n\r][\u00A0\u2007\u202F\s])*+'
                        r'(?:[\n\r|\r\n|\n|\r]+)'
                        r'(?:[\u00A0\u2007\u202F\s][^\n\r]|[^\n\r][\u00A0\u2007\u202F\s])*+'), "Split", {"kind": "external"})
        ]


# from GATE default tokenizer
modified_gate_tokenizer_rules = r"""
#words#
// a word can be any combination of letters, including hyphens,
// but excluding symbols and punctuation, e.g. apostrophes
// Note that there is an alternative version of the tokeniser that
// treats hyphens as separate tokens
|(?:\p{Lu}(?:\p{Mn})*)(?:(?:\p{Ll}(?:\p{Mn})*)(?:(?:\p{Ll}(?:\p{Mn})*)|\p{Pd}|\p{Cf})*)*
0 =>  Token orth="upperInitial", kind="word",
|(?:\p{Lu}(?:\p{Mn})*)(?:\p{Pd}|\p{Cf})*(?:(?:\p{Lu}(?:\p{Mn})*)|\p{Pd}|\p{Cf})+
0 =>  Token orth="allCaps", kind="word",
|(?:\p{Ll}(?:\p{Mn})*)(?:(?:\p{Ll}(?:\p{Mn})*)|\p{Pd}|\p{Cf})*
0 =>  Token orth="lowercase", kind="word",
// MixedCaps is any mixture of caps and small letters that doesn't
// fit in the preceding categories
|(?:(?:\p{Ll}(?:\p{Mn})*)(?:\p{Ll}(?:\p{Mn})*)+(?:\p{Lu}(?:\p{Mn})*)+(?:(?:\p{Lu}(?:\p{Mn})*)|(?:\p{Ll}(?:\p{Mn})*))*)|(?:(?:\p{Ll}(?:\p{Mn})*)(?:\p{Ll}(?:\p{Mn})*)*(?:\p{Lu}(?:\p{Mn})*)+(?:(?:\p{Lu}(?:\p{Mn})*)|(?:\p{Ll}(?:\p{Mn})*)|\p{Pd}|\p{Cf})*)|(?:(?:\p{Lu}(?:\p{Mn})*)(?:\p{Pd})*(?:\p{Lu}(?:\p{Mn})*)(?:(?:\p{Lu}(?:\p{Mn})*)|(?:\p{Ll}(?:\p{Mn})*)|\p{Pd}|\p{Cf})*(?:(?:\p{Ll}(?:\p{Mn})*))+(?:(?:\p{Lu}(?:\p{Mn})*)|(?:\p{Ll}(?:\p{Mn})*)|\p{Pd}|\p{Cf})*)|(?:(?:\p{Lu}(?:\p{Mn})*)(?:\p{Ll}(?:\p{Mn})*)+(?:(?:\p{Lu}(?:\p{Mn})*)+(?:\p{Ll}(?:\p{Mn})*)+)+)|(?:(?:(?:\p{Lu}(?:\p{Mn})*))+(?:(?:\p{Ll}(?:\p{Mn})*))+(?:(?:\p{Lu}(?:\p{Mn})*))+)
0 =>  Token orth="mixedCaps", kind="word",
|(?:\p{Lo}|\p{Mc}|\p{Mn})+
0 => Token kind="word", type="other",
#numbers#
// a number is any combination of digits - altered from default GATE rule
|(?:[0-9]*[.])?[0-9]+(?:[eE^][-+]?[0-9]+)?
0 => Numeric kind="number",
|\p{No}+
0 => Token kind="number",
#whitespace#
|(?:\p{Zs})
0 => SpaceToken kind="space",
|(?:\p{Cc})
0 => SpaceToken kind="control",
#symbols#
|(?:\p{Sk}|\p{Sm}|\p{So})
0 =>  Token kind="symbol",
|\p{Sc}
0 =>  Token kind="symbol", symbolkind="currency",
#punctuation#
|(?:\p{Pd}|\p{Cf})
0 => Token kind="punctuation", subkind="dashpunct",
|(?:\p{Pc}|\p{Po})
0 => Token kind="punctuation",
|(?:\p{Ps}|\p{Pi})
0 => Token kind="punctuation", position="startpunct",
|(?:\p{Pe}|\p{Pf})
0 => Token kind="punctuation", position="endpunct",
"""