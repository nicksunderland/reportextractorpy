from gatenlp import Document
from gatenlp.processing.pipeline import Pipeline
from gatenlp.processing.gazetteer import StringGazetteer  # TokenGazetteer, StringRegexAnnotator
from gatenlp.processing.tokenizer import NLTKTokenizer
from nltk.tokenize.regexp import WordPunctTokenizer
from reportextractorpy.utils import Utils
from os import path
from yaml import safe_load

from gatenlp.pam.pampac import PampacAnnotator, Pampac, Rule
from gatenlp.pam.pampac import Ann, AnnAt, Or, And, Filter, Find, Lookahead, N, Seq, Text
from gatenlp.pam.pampac import AddAnn, UpdateAnnFeatures
from gatenlp.pam.pampac import GetAnn, GetEnd, GetFeature, GetFeatures, GetRegexGroup, GetStart, GetText, GetType
from gatenlp.pam.matcher import isIn, IfNot, Nocase


class DataProcessing:
    def __init__(self, mode):
        self.mode = mode
        self.data_dict = self.__gen_data_dict()

        # ?add nltk_sent_tokenizer=RegexpTokenizer() to NLTKTokenizer below?
        # internal sentence splits: (?:\.){1,3}"?|(?:!|\?){1,4}"?
        # external sentence splits: ???
        # non-split patterns
        self.tokenizer = NLTKTokenizer(nltk_tokenizer=WordPunctTokenizer(),
                                       token_type="Token")
        self.str_gaz_case_sens = self.__gen_str_gazetteer(case_sens=True)
        self.str_gaz_case_insens = self.__gen_str_gazetteer(case_sens=False)
        self.pattern_matcher = self.__gen_pattern_annotator()
        print(self)

    def run(self):
        docs = [Document(self.example_text()), Document(self.example_text())]

        pipeline = Pipeline((self.tokenizer, "Tokenizer"),
                            (self.str_gaz_case_sens, "Gazetteer - case sensitive"),
                            (self.str_gaz_case_insens, "Gazetteer - case insensitive"),
                            (self.pattern_matcher, "PAMPAC annotator"))

        docs = pipeline.pipe(docs)

        for i, doc in enumerate(docs):
            defset = doc.anns(("", ["Anatomy", "Token"]))
            custset = doc.annset(self.mode)
            print("Doc #" + str(i))
            print(doc)
            print(defset)
            print(custset)

        #rep = Report("echocardiogram", "ID_100000", datetime(2000, 10, 10, 0, 0, 0), "some sample report text")

    @staticmethod
    def foo_func(text):
        print("here")
        print(text)
        print(type(text))
        return str(text) + "_helloWorld"

    def __gen_pattern_annotator(self) -> PampacAnnotator:
        pat1 = Seq(Ann("Token"),
                   AnnAt("Anatomy", name="anat1"),
                   AnnAt("Anatomy", name="anat2"),
                   AnnAt("Token"))
        action1 = AddAnn(type="PATTERN1",
                         features={"foo0": GetText(),
                                   "foo2": GetText("anat1"),
                                   "func": GetText("anat2"),
                                   "foo4": GetType("anat1"),
                                   "foo5": GetFeature("anat1", "major")})
        rule1 = Rule(pat1, action1)
        pampac1 = Pampac(rule1, skip="longest", select="first")
        pattern_annotator = PampacAnnotator(pampac1,
                                            annspec=[("", ["Anatomy", "Token"])],
                                            outset_name=self.mode)
        return pattern_annotator

    @staticmethod
    def __gen_str_gazetteer(case_sens: bool = True) -> StringGazetteer:
        if case_sens:
            gazetteer = StringGazetteer(longest_only=True, ws_clean=True, map_chars=None)
        else:
            gazetteer = StringGazetteer(longest_only=True, ws_clean=True, map_chars="lower")
        for fp in Utils.gazetteer_config_files():
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

    def __gen_data_dict(self) -> dict:
        config_path = path.join(Utils.configs_path(), self.mode + ".yml")
        with open(config_path) as f:
            config = safe_load(f)
            return config

    @staticmethod
    def example_text():
        return """token sov stj token"""
 #
 # Report:
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
               "\tData dict: {1}".format(self.mode, self.data_dict))
