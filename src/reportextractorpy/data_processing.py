import regex
from gatenlp import Document
from reportextractorpy.nlp_resources.tokenizer.custom_tokenizer import CustomTokenizer
from gatenlp.processing.gazetteer import StringRegexAnnotator
from gatenlp.processing.pipeline import Pipeline
from gatenlp.pam.pampac import Rule, PampacAnnotator, Pampac
from gatenlp.pam.pampac import AnnAt, Or, N
from gatenlp.pam.pampac import AddAnn
from gatenlp.processing.tokenizer import NLTKTokenizer
from PyQt5 import QtCore
from typing import List
from reportextractorpy.utils import Utils
from os import path
from yaml import safe_load
from importlib import import_module
from gatenlp.pam.pampac import PampacAnnotator
import re
import regex


class DataProcessing(QtCore.QObject):
    # signals
    load_complete_signal = QtCore.pyqtSignal(int)  # int: number of docs loaded, or available to process
    processing_complete_signal = QtCore.pyqtSignal(Document)

    def __init__(self, mode):
        QtCore.QObject.__init__(self)
        self.mode = mode
        self.data_dict = self._gen_data_dict()
        self.processing_pipeline = self._gen_pipeline()
        self.docs = []
        print(self)

    def run(self, index: List[int] | str = "all"):
        assert any([all(isinstance(x, int) for x in index), index == "all"])

        if index == "all" or len(index) > 1:
            print("TODO: separate run method for running all of the docs (and not emitting until the end)")
            # TODO: separate run method for running all of the docs (and not emitting until the end)
        else:
            docs = [self.docs[i] for i in index]
            doc = self.processing_pipeline.pipe(docs)
            d = next(doc)  # remember the processing only gets called with next()
            self.processing_complete_signal.emit(d)

    def load(self, input_str: str, option: str):
        if option == "string":
            self.docs = [Document(input_str)]
        elif option == "csv":
            # TODO: csv loading
            pass
        elif option == "dir":
            # TODO: directory csv loading
            pass
        # int: number of docs loaded, or available to process
        self.load_complete_signal.emit(len(self.docs))

    def _gen_pipeline(self):
        # Regex TOKENIZER (uses modified GATE token regexes to split on)
        tokenizer = StringRegexAnnotator(source=CustomTokenizer().formatted_regex_rules(),
                                         source_fmt="string",
                                         select_rules="all",
                                         longest_only=True,
                                         skip_longest=True,
                                         regex_module="regex")

        # Regex GAZEETTER
        regex_gazetteer = StringRegexAnnotator(source=None,
                                               source_fmt="string",
                                               select_rules="all",
                                               longest_only=True,
                                               skip_longest=True,
                                               regex_module="regex")
        gazetteer_configs = Utils.parse_gazetteer_configs(self.mode)
        for mod, f, regex_rules in gazetteer_configs:
            regex_gazetteer.append(source=regex_rules, source_fmt="string")

        # Sentence tokenizer
        pattern_sent = N(Or(AnnAt(type=re.compile(r'^(?!Split$)')),
                            AnnAt(type="Split").within(type=re.compile(r'^(?!Split$)'))), min=1, max=40)
        action_sent = AddAnn(type="Sentence")
        rule_sent = Rule(pattern_sent, action_sent)
        pampac = Pampac(rule_sent, skip="longest", select="first")
        sent_tokenizer = PampacAnnotator(pampac, annspec="", outset_name="")

        # Patterns
        pattern_modules = Utils.pattern_modules_list(self.mode)
        pattern_annotators = []
        for module in pattern_modules:
            pattern_module = getattr(import_module(module), "Pattern")
            print("\033[92mImport pattern module: " + module + "\033[0m")
            for annotator in pattern_module():
                pattern_annotators.append(annotator)

        return Pipeline(tokenizer,
                        regex_gazetteer,
                        sent_tokenizer,
                        *pattern_annotators)

    def _gen_data_dict(self) -> dict:
        config_path = path.join(Utils.configs_path(), self.mode + ".yml")
        with open(config_path) as f:
            config = safe_load(f)
            return config

    def __str__(self):
        return("-----------------------------------\n"
               "DataProcessing object:\n"
               "\tMode:      {0}\n"
               "\tPipeline:  add stuff here\n"
               "\tData dict: {1}".format(self.mode, self.data_dict))
