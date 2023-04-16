from gatenlp import Document
from gatenlp.processing.gazetteer import StringGazetteer  # TokenGazetteer, StringRegexAnnotator
from gatenlp.processing.tokenizer import NLTKTokenizer
from nltk.tokenize.regexp import WordPunctTokenizer
from reportextractorpy.report import Report
from reportextractorpy.utils import Utils
from datetime import datetime

from yaml import safe_load


class DataProcessing:
    def __init__(self):
        self.tokenizer = NLTKTokenizer(nltk_tokenizer=WordPunctTokenizer(), token_type="Token", outset_name="")
        self.str_gaz_case_sens = self.__gen_str_gazetteer(case_sens=True)
        self.str_gaz_case_insens = self.__gen_str_gazetteer(case_sens=False)

    def run(self):
        doc = Document(self.example_text())
        doc = self.tokenizer(doc)
        doc = self.str_gaz_case_sens(doc)
        doc = self.str_gaz_case_insens(doc)
        defset = doc.annset()
        custset = doc.annset("echocardiogram")
        print(defset)
        print(custset)
        #rep = Report("echocardiogram", "ID_100000", datetime(2000, 10, 10, 0, 0, 0), "some sample report text")

    @staticmethod
    def __gen_str_gazetteer(case_sens: bool = True) -> StringGazetteer:

        if case_sens:
            gazetteer = StringGazetteer(outset_name="echocardiogram", longest_only=True, ws_clean=True, map_chars=None)
        else:
            gazetteer = StringGazetteer(outset_name="echocardiogram", longest_only=True, ws_clean=True, map_chars="lower")

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

    @staticmethod
    def example_text():
        return """Report:
 Left ventricle:
 The left ventricle is seen to contract uniformly well in systole.  No regional wall motion abnormalities are identified.
 No left ventricular dilatation.  Mild concentric left ventricular hypertrophy.
 
 Measurements:
 I V S 1.2 cm.  EDD 4.4 cm.  PW 1.2 cm.  ESD 3.1 cm.
 E A ratio 1.21.  E wave deceleration time 173 milliseconds.
 Septal E' 7 cm/sec.  Lateral E' 8 cm/sec.
 Septal S' 7 cm/sec.  Lateral S' to 9 cm/sec.
 E/E' 15.
 Septal MAPSE 12 mm.  Lateral MAPSE 14 mm.
 
 Mitral valve:
 Mobile mitral valve leaflets seen to open well.  No mitral stenosis no mitral regurgitation.
 
 Left atrium:
 The left atrium measures 35 cm2.
 
 Aortic valve:
 Trileaflet valve.  No aortic stenosis, AV V-max 1.3 metres per second.  No aortic regurgitation.
 Aortic root dimensions are within normal limits.
 sinus of valsalva 3cm.
 stj is 3cm.
 asc Ao. is 4cm.
 No coarctation.
 
 Right-sided structures:
 Right ventricle contracts well and is not dilated, TAPSE 23 mm.  The right atrium is not dilated.
 No measurable tricuspid regurgitation identified.
 Normal pulmonary valve Doppler profile.
 Normal appearance of the inferior vena cava with good compliance.
 
 Summary:
 Good left ventricular systolic function.
 Difficult to quantify diastolic function probably stage II with high left ventricular filling pressures.
 Mild concentric left ventricular hypertrophy.
 Moderate left atrial dilatation.
 No gross valvular lesion demonstrated."""