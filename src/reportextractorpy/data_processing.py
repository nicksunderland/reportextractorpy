from reportextractorpy.nlp_resources.tokenizer.custom_tokenizer import CustomTokenizer
from reportextractorpy.utils import Utils
from gatenlp import Document
from gatenlp.corpora import ListCorpus
from gatenlp.processing.gazetteer import StringRegexAnnotator
from gatenlp.processing.pipeline import Pipeline
from gatenlp.processing.executor import SerialCorpusExecutor
from pyclbr import readmodule
from gatenlp.pam.pampac import Rule, Pampac, PampacAnnotator, AnnAt, Or, N, AddAnn, And
from gatenlp.pam.matcher import FeatureMatcher, IfNot
from PyQt5 import QtCore
from os import path
from yaml import safe_load
from importlib import import_module
import re


class DataProcessing(QtCore.QObject):
    # signals
    load_complete_signal = QtCore.pyqtSignal(int)  # int: number of docs loaded, or available to process
    processing_complete_signal = QtCore.pyqtSignal(Document)

    def __init__(self, mode):
        QtCore.QObject.__init__(self)
        self.mode = mode
        self.data_dict = self._gen_data_dict()
        self.processing_pipeline = self._gen_pipeline()
        self.corpus = ListCorpus([])
        print(self)

    def run(self, index: int | str = "all"):
        assert isinstance(index, int) or index == "all"

        if index == "all":
            print("TODO: separate run method for running all of the docs (and not emitting until the end)")
            # TODO: separate run method for running all of the docs (and not emitting until the end)
        else:
            try:
                doc = self.corpus[index]
                doc = self.processing_pipeline(doc)
                self.processing_complete_signal.emit(doc)
                return doc
            except IndexError:
                print(f'Index error in DataProcessing.run() with index {index} but corpus only containing '
                      f'{len(self.corpus)} documents')
                exit()

    def load(self, input_str: str, option: str):
        assert option in ["string", "csv", "dir"]
        if option == "string":
            self.corpus = ListCorpus([Document(input_str)])
        elif option == "csv":
            # TODO: csv loading
            pass
        elif option == "dir":
            # TODO: directory csv loading
            pass
        # int: number of docs loaded, or available to process
        num_docs = len(self.corpus)
        self.load_complete_signal.emit(num_docs)
        if num_docs > 0:
            self.run(index=0)

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
        pattern_sent = N(Or(AnnAt().notat(type="Split"),
                            AnnAt(type="Split").within(type=re.compile(r'^(?!Split$|Token$)'))), min=1, max=40)
        action_sent = AddAnn(type="Sentence")
        rule_sent = Rule(pattern_sent, action_sent)
        pampac = Pampac(rule_sent, skip="longest", select="first")
        sent_tokenizer = PampacAnnotator(pampac, annspec="", outset_name="")

        # Patterns
        pattern_modules = Utils.pattern_modules_list(self.mode)  # get all the pattern .py files / modules
        pattern_annotators = []
        for module in pattern_modules:  # for each pattern module
            module_info = readmodule(module)  # read the .py file (but doesn't import) to a dictionary
            for cls_name, mod in module_info.items():  # for each class/phase defined in the module
                if "AbstractPatternAnnotator" in mod.super:  # if the class inherits AbstractPatternAnnotator
                    pattern_module = getattr(import_module(module), cls_name)  # actually import the specific class/phase
                    for template_idx, annotator in enumerate(pattern_module(outset_name=self.mode)):  # each class might be a generator which produces templated phases
                        pattern_annotators.append(annotator)  # add the phase to the list
                        print(f"\033[92mImport pattern class {cls_name}, template {template_idx}, from module {module} \033[0m")
                else:
                    raise Exception(
                        f'\n\tTrying to import a pattern module containing a class named \'{cls_name}\'\n'
                        f'\tfrom module \'{module}\'\n'
                        f'\tbut the class \'{cls_name}\' does not inherit from AbstractPatternAnnotator'
                    )

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
