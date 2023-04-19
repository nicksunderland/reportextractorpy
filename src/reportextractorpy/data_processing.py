from gatenlp import Document
from gatenlp.processing.pipeline import Pipeline
from gatenlp.processing.gazetteer import StringGazetteer  # TokenGazetteer, StringRegexAnnotator
from gatenlp.processing.tokenizer import NLTKTokenizer
from nltk.tokenize import WordPunctTokenizer
from typing import List
import reportextractorpy.nlp_resources
from reportextractorpy.utils import Utils
from os import path
from yaml import safe_load
import pickle
import sys
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from gatenlp.pam.pampac import PampacAnnotator


class DataProcessing:
    def __init__(self, mode):
        self.mode = mode
        self.data_dict = self._gen_data_dict()
        self.tokenizer = self._gen_tokenizer()
        self.sent_tokenizer = self._gen_sent_tokenizer()
        self.str_gaz_case_sens = self._gen_str_gazetteer(case_sens=True)
        self.str_gaz_case_insens = self._gen_str_gazetteer(case_sens=False)
        self.pattern_annotators = self._gen_pattern_annotators()
        print(self)

    def run(self):
        docs = [Document(self.example_text()), Document(self.example_text())]

        pipeline = Pipeline(self.tokenizer,
                            self.sent_tokenizer,
                            self.str_gaz_case_sens,
                            self.str_gaz_case_insens,
                            *self.pattern_annotators)

        docs = pipeline.pipe(docs)

        for i, doc in enumerate(docs):
            print(doc)
            allset = doc.annset()  # ([("", ["Anatomy", "Token"])])
            defset = doc.anns([("", ["Anatomy", "Token"])])
            custset = doc.annset(self.mode)
            print("Doc #" + str(i))
            print("Allset:  " + str(allset))
            print("Defset:  " + str(defset))
            print("Custset: " + str(custset))
            break

        #rep = Report("echocardiogram", "ID_100000", datetime(2000, 10, 10, 0, 0, 0), "some sample report text")

    @staticmethod
    def _gen_tokenizer() -> NLTKTokenizer:
        return NLTKTokenizer(nltk_tokenizer=WordPunctTokenizer(),
                             token_type="Token",
                             space_token_type="Space")

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
        for fp in Utils.gazetteer_config_files(self.mode):
            with open(fp) as f:
                gaz_config = safe_load(f)
                ci = gaz_config["string_gazetteer"]["case_insens_matches"]
                cs = gaz_config["string_gazetteer"]["case_sens_matches"]
                phrases = [item.rstrip(".") for sublist in [ci, cs] if sublist is not None
                           for item in sublist if "." in item]
                [extra_abbreviations.update(extract_recursive(phr)) for phr in phrases]
        sent_tokenizer._params.abbrev_types.update(extra_abbreviations)

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
        if case_sens:
            gazetteer = StringGazetteer(longest_only=True, ws_clean=True, map_chars=None)
        else:
            gazetteer = StringGazetteer(longest_only=True, ws_clean=True, map_chars="lower")
        for fp in Utils.gazetteer_config_files(self.mode):
            with open(fp) as f:
                gaz_config = safe_load(f)

                if case_sens:
                    matches = gaz_config["string_gazetteer"]["case_sens_matches"]
                else:
                    matches = gaz_config["string_gazetteer"]["case_insens_matches"]

                gazlist = [(m, None) for m in (matches if matches is not None else [])]
                gazetteer.append(source=gazlist,
                                 source_fmt="gazlist",
                                 list_type=gaz_config["annot_type"],
                                 list_features=gaz_config["annot_features"])
        return gazetteer

    def _gen_data_dict(self) -> dict:
        config_path = path.join(Utils.configs_path(), self.mode + ".yml")
        with open(config_path) as f:
            config = safe_load(f)
            return config

    @staticmethod
    def example_text():
        return """Text: this sov 3 cm"""


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
