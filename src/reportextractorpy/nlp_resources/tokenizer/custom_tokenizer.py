from reportextractorpy.abstract_gazetteer import AbstractGazetteer
import regex
import re


class CustomTokenizer(AbstractGazetteer):
    annot_type = "Token"
    annot_features = {"kind": "word"}
    regex_rules = [
        regex.compile(r'(?:\p{Ll}(?:\p{Mn})*)(?:(?:\p{Ll}(?:\p{Mn})*)|\p{Pd}|\p{Cf})*', flags=regex.I),
        (regex.compile(r'(?:[0-9]*[.])?[0-9]+(?:[eE^][-+]?[0-9]+)?'), "Token", {"kind": "numeric"}),
        (regex.compile(r'(?:\p{Zs})'), "SpaceToken", {"kind": "space"}),
        (regex.compile(r'(?:\p{Cc})'), "SpaceToken", {"kind": "control"}),
        (regex.compile(r'(?:\p{Sk}|\p{Sm}|\p{So})'), "Token", {"kind": "symbol"}),
        (regex.compile(r'(?:\p{Sk}|\p{Sm}|\p{So})'), "Token", {"kind": "symbol", "symbolkind": "currency"}),
        (regex.compile(r'(?:\p{Pd}|\p{Cf})'), "Token", {"kind": "punctuation", "subkind": "dashpunct"}),
        #(regex.compile(r'(?:\p{Pc}|\p{Po})'), "Token", {"kind": "punctuation"}),
        (regex.compile(r'(?:\p{Ps}|\p{Pi})'), "Token", {"kind": "punctuation", "position": "startpunct"}),
        (regex.compile(r'(?:\p{Pe}|\p{Pf})'), "Token", {"kind": "punctuation", "position": "endpunct"}),
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
