import regex
from gatenlp import Document
from reportextractorpy.nlp_resources.tokenizer.sentence_tokenizer import SentenceTokenizer
from reportextractorpy.nlp_resources.tokenizer.custom_tokenizer import CustomTokenizer #, modified_gate_tokenizer_rules
from gatenlp.processing.gazetteer import StringRegexAnnotator
from gatenlp.processing.pipeline import Pipeline
from gatenlp.processing.tokenizer import NLTKTokenizer
from PyQt5 import QtCore
from typing import List
from reportextractorpy.utils import Utils
from os import path
from yaml import safe_load
import pickle
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
        self.regex_tokenizer = self._gen_regex_tokenizer()
        self.sent_tokenizer = SentenceTokenizer()
        self.regex_gazetteer = self._gen_regex_gazetteer()
        self.pattern_annotators = self._gen_pattern_annotators()
        self.docs = []
        print(self)

    def run(self, index: List[int] | str = "all"):
        assert any([all(isinstance(x, int) for x in index), index == "all"])

        pipeline = Pipeline(self.regex_tokenizer,
                            self.regex_gazetteer,
                            self.sent_tokenizer,
                            *self.pattern_annotators)

        if index == "all" or len(index) > 1:
            print("TODO: separate run method for running all of the docs (and not emitting until the end)")
            # TODO: separate run method for running all of the docs (and not emitting until the end)
        else:
            docs = [self.docs[i] for i in index]
            doc = pipeline.pipe(docs)
            d = next(doc)
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

    def _gen_pattern_annotators(self) -> List[PampacAnnotator]:
        pattern_modules = Utils.pattern_modules_list(self.mode)
        annotators = []
        for module in pattern_modules:
            pattern_class = getattr(import_module(module), "Pattern")
            pat_annotator = pattern_class(self.mode)
            annotators.append(pat_annotator)
        return annotators

    def _gen_regex_tokenizer(self) -> StringRegexAnnotator:
        cust_tok = CustomTokenizer()
        tokenizer = StringRegexAnnotator(source=CustomTokenizer.formatted_regex_rules(cust_tok),
                                         source_fmt="string",
                                         select_rules="all",
                                         longest_only=True,
                                         skip_longest=True,
                                         regex_module="regex")
        return tokenizer

    def _gen_regex_gazetteer(self) -> StringRegexAnnotator:
        regex_gazetteer = StringRegexAnnotator(source=None,
                                               source_fmt="string",
                                               select_rules="all",
                                               longest_only=True,
                                               skip_longest=True,
                                               regex_module="regex")

        # Load the StringRegexAnnotator
        gazetteer_configs = Utils.parse_gazetteer_configs(self.mode)
        for mod, f, regex_rules in gazetteer_configs:
            regex_gazetteer.append(source=regex_rules, source_fmt="string")

        return regex_gazetteer

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
