from gatenlp import Document
from gatenlp.processing.pipeline import Pipeline
from gatenlp.processing.gazetteer import StringGazetteer, StringRegexAnnotator
from reportextractorpy.nlp_resources.tokenizer.custom_tokenizer import custom_tokenizer_rules
from gatenlp.processing.tokenizer import NLTKTokenizer
from typing import List
from spacy.language import Language
from numerizer import spacy_numerize
from reportextractorpy.utils import Utils
from os import path
from yaml import safe_load
import pickle
from importlib import import_module
from gatenlp.pam.pampac import PampacAnnotator


class DataProcessing:
    def __init__(self, mode):
        self.mode = mode
        self.data_dict = self._gen_data_dict()
        self.str_gazetter = self._gen_str_gazetteer()
        self.regex_tokenizer = self._gen_regex_tokenizer()
        self.sent_tokenizer = self._gen_sent_tokenizer()
        self.pattern_annotators = self._gen_pattern_annotators()

        print(self)

    @staticmethod
    @Language.component("numerize")
    def numerize(doc, labels='all', retokenize=True):
        # https://spacy.io/api/attributes
        return spacy_numerize(doc, labels, retokenize)

    def run(self):
        docs = [Document(self.example_text()), Document(self.example_text())]

        pipeline = Pipeline(self.regex_tokenizer,
                            self.sent_tokenizer,
                            self.str_gazetter,
                            *self.pattern_annotators)

        docs = pipeline.pipe(docs)



        for i, doc in enumerate(docs):
            print(doc)
            print("Matching:", [doc[a] for a in doc.annset()])
            allset = doc.annset()  # ([("", ["Anatomy", "Token"])])
            defset = doc.anns([("", ["Anatomy", "Token", "Units"])])
            custset = doc.annset(self.mode)
            print("Doc #" + str(i))
            print("Allset:  ")# + str(allset))
            for a in allset:
                print("\t'" + str(a) + "' - " + doc[a])
            print("Defset:  " + str(defset))
            print("Custset: ")
            for a in custset:
                print("\t'" + str(a) + "' - " + doc[a])
            break

    def _gen_sent_tokenizer(self) -> NLTKTokenizer:
        sent_tokenizer_fp = path.join(Utils.nlp_resources_path(),
                                      "tokenizer",
                                      "nltk_punktsentencetokenizer_english.pickle")

        # Load the pre-trained NLTK PunktSentenceTokenizer
        with open(sent_tokenizer_fp, "rb") as resource_file:
            sent_tokenizer = pickle.load(resource_file)

        # Need to split phrase with multiple periods (and spaces) into constituent parts
        def extract_recursive(s):
            head, sep, tail = s.partition('. ')
            if tail == "":
                return [head.strip().rstrip(".")]
            else:
                return [head.strip()] + extract_recursive(tail.strip())

        # Add the extra sentence split info to the NLTK PunktSentenceTokenizer
        extra_abbreviations = set()
        gazetteer_configs = Utils.parse_gazetteer_configs(self.mode)
        for _, _, string_matches, _ in gazetteer_configs:
            phrases = [item.rstrip(".") for item in string_matches if "." in item]
            [extra_abbreviations.update(extract_recursive(phr)) for phr in phrases]
            sent_tokenizer._params.abbrev_types.update(extra_abbreviations)

        #return sent_tokenizer
        return NLTKTokenizer(nltk_tokenizer=sent_tokenizer, token_type="Sentence")

    def _gen_pattern_annotators(self) -> List[PampacAnnotator]:
        pattern_modules = Utils.pattern_modules_list(self.mode)
        annotators = []
        for module in pattern_modules:
            pattern_class = getattr(import_module(module), "Pattern")
            pat_annotator = pattern_class(self.mode)
            annotators.append(pat_annotator)
        return annotators

    def _gen_str_gazetteer(self, case_sens: bool = True) -> StringGazetteer:
        str_gazetteer = StringGazetteer(longest_only=True, ws_clean=True, map_chars="lower")

        # Load the StringGazetteer
        gazetteer_configs = Utils.parse_gazetteer_configs(self.mode)
        for annot_type, features, string_matches, _ in gazetteer_configs:
            gaz_list = [(m, None) for m in (string_matches if string_matches is not None else [])]
            str_gazetteer.append(source=gaz_list,
                                 source_fmt="gazlist",
                                 list_type=annot_type,
                                 list_features=features)
        return str_gazetteer

    def _gen_regex_tokenizer(self) -> StringRegexAnnotator:

        regex_gazetteer = StringRegexAnnotator(source=custom_tokenizer_rules,
                                               source_fmt="string",
                                               select_rules="all",
                                               skip_longest=True,
                                               longest_only=True,
                                               regex_module="regex")

        # Load the StringRegexAnnotator
        gazetteer_configs = Utils.parse_gazetteer_configs(self.mode)
        for annot_type, features, string_matches, regex_rules in gazetteer_configs:
            regex_gazetteer.append(source=regex_rules,
                                   source_fmt="string",
                                   list_features=features)
        return regex_gazetteer

    def _gen_data_dict(self) -> dict:
        config_path = path.join(Utils.configs_path(), self.mode + ".yml")
        with open(config_path) as f:
            config = safe_load(f)
            return config

    @staticmethod
    def example_text():
        return """sov 3.1 cm. sov 3.5-4.5 cm. sov 3.5 4.5 cm. sinus of valsalva. dog123. 5.6, 66.56, 1^5, 4e5"""



 #        Report:
 # Left ventricle:
 # The left ventricle is seen to contract uniformly well in systole.  No regional wall motion abnormalities are identified.
 # No left ventricular dilatation.  Mild concentric left ventricular hypertrophy.
 #
 # Measurements:
 # I V S 1.2 cm.  EDD 4.4 cm.  PW 1.2 cm.  ESD 3.1 cm.
 # E A ratio 1.21.  E wave deceleration time 173 milliseconds.
 # Septal E' 7 cm/sec.  Lateral E' 8 cm/sec.
 # Septal S' 7 cm/sec.  Lateral S' to 9 cm/sec.
 # E/E' 15.
 # Septal MAPSE 12 mm.  Lateral MAPSE 14 mm.
 #
 # Mitral valve:
 # Mobile mitral valve leaflets seen to open well.  No mitral stenosis no mitral regurgitation.
 #
 # Left atrium:
 # The left atrium measures 35 cm2.
 #
 # Aortic valve:
 # Trileaflet valve.  No aortic stenosis, AV V-max 1.3 metres per second.  No aortic regurgitation.
 # Aortic root dimensions are within normal limits.
 # sinus of valsalva 3cm.
 # stj is 3cm.
 # asc Ao. is 4cm.
 # No coarctation.
 #
 # Right-sided structures:
 # Right ventricle contracts well and is not dilated, TAPSE 23 mm.  The right atrium is not dilated.
 # No measurable tricuspid regurgitation identified.
 # Normal pulmonary valve Doppler profile.
 # Normal appearance of the inferior vena cava with good compliance.
 #
 # Summary:
 # Good left ventricular systolic function.
 # Difficult to quantify diastolic function probably stage II with high left ventricular filling pressures.
 # Mild concentric left ventricular hypertrophy.
 # Moderate left atrial dilatation.
 # No gross valvular lesion demonstrated."""

    def __str__(self):
        return("-----------------------------------\n"
               "DataProcessing object:\n"
               "\tMode:      {0}\n"
               "\tPipeline:  add stuff here\n"
               "\tData dict: {1}".format(self.mode, self.data_dict))
