"""
This is a straight copy from the GATE NLP Python repository, as I need to use a slightly
altered javascript functions
Module that implements the various ways of how to save and load documents and change logs.
"""
import os
from gatenlp.document import Document
from gatenlp.gatenlpconfig import gatenlpconfig
import json as jsonlib

HTML_TEMPLATE_FILE_NAME = "gatenlp-ann-viewer.html"
JS_GATENLP_FILE_NAME = "gatenlp-ann-viewer-merged.js"
SEP = "║"


class CustomHtmlAnnViewerSerializer:
    """
    Serialization class for generating HTML/Javascript to view a document in an HTML page or in a Jupyter or
    Colab notebook.
    """

    @staticmethod
    def javascript():
        """
        Return the Javascript needed for the HTML Annotation viewer.

        Returns: Javascript string.

        """
        jsloc = os.path.join(
            os.path.dirname(__file__), "ui_resources", JS_GATENLP_FILE_NAME
        )
        if not os.path.exists(jsloc):
            raise Exception(
                "Could not find JavsScript file, {} does not exist".format(jsloc)
            )
        with open(jsloc, "rt", encoding="utf-8") as infp:
            js = infp.read()
            js = """<script type="text/javascript">""" + js + "</script>"
        return js

    @staticmethod
    def convert_to_html(doc,
                        stretch_height=False,
                        annspec=None,
                        preselect=None,
                        palette=None,
                        cols4types=None,
                        doc_style=None,
                        row1_style=None,
                        row2_style=None):
        """Convert a document to HTML for visualizing it.

        Args:
            doc: the current Document instance/object to save
            _clazz: the class of the object to save
            stretch_height: if False, rows 1 and 2 of the viewer will not have the height set, but only
                min and max height (default min is 10em for row1 and 7em for row2, max is the double of those).
                If True, no max haight is set and instead the height is set to a percentage (default is
                67vh for row 1 and 30vh for row 2). The values used can be changed via gateconfig or the
                complete style for the rows can be set directly via row1_style and row2_style.
            annspec: if None, include all annotation sets and types, otherwise this should be a list of either
                set names, or tuples, where the first entry is a set name and the second entry is either a type
                name or list of type names to include.
            preselect: if not None, the set and type names to pre-select (show). This should have the same format
                as the annspec parameter.
            palette: if not None a list of colour codes (strings) usable in Javascript which will be used instead
                of the default palette.
            cols4types: if not None a dictionary mapping tuples (setname, typename) to a color. For the given
                setname and typename combinations, the colours from the palette (default or specified) will be
                overrriden.
            doc_style: if not None, any additional styling for the document text box, if None, use whatever
                is defined as gatenlpconfig.doc_html_repr_doc_style or do not use.
            row1_style: the style to use for the first row of the document viewer which shows the document text and
                annotation set and type panes. The default is gatenlpconfig.doc_html_repr_row1style_nostretch or
                gatenlpconfig.doc_html_repr_row1style_nostretch depending on the stretch_height parameter.
            row2_style: the style to use for the second row of the document viewer which shows the document or
                annotation features. The default is gatenlpconfig.doc_html_repr_row2style_nostretch or
                gatenlpconfig.doc_html_repr_row2style_nostretch depending on the stretch_height parameter.
            kwargs: swallow any other kwargs.

        Returns: if to_mem is True, returns the representation, otherwise None.

        """
        if not isinstance(doc, Document):
            raise Exception("Not a document!")
        parms = dict(presel_set=[], presel_list=[])
        doccopy = doc.deepcopy(annspec=annspec)
        doccopy.to_offset_type("j")
        json = doccopy.save_mem(fmt="json")
        htmlloc = os.path.join(
            os.path.dirname(__file__), "ui_resources", HTML_TEMPLATE_FILE_NAME
        )
        if not os.path.exists(htmlloc):
            raise Exception(
                "Could not find HTML template, {} does not exist".format(htmlloc)
            )
        with open(htmlloc, "rt", encoding="utf-8") as infp:
            html = infp.read()
        txtcolor = gatenlpconfig.doc_html_repr_txtcolor
        if preselect is not None:
            # create a list of set/type lists and a set of set of setSEPtype for parms
            presel_set = set()
            presel_list = []
            for el in preselect:
                if isinstance(el, str):
                    for anntype in doccopy.annset(el).type_names:
                        settype = el + SEP + anntype
                        if settype not in presel_set:
                            presel_set.add(settype)
                            presel_list.append([el, anntype])
                elif isinstance(el, (list, tuple)) and len(el) > 1:
                    setname = el[0]
                    anntypes = el[1]
                    if isinstance(anntypes, str):
                        anntypes = [anntypes]
                    for anntype in anntypes:
                        settype = setname + SEP + anntype
                        if settype not in presel_set:
                            presel_set.add(settype)
                            presel_list.append([setname, anntype])
            parms["presel_set"] = list(presel_set)
            parms["presel_list"] = presel_list
        if palette is not None:
            parms["palette"] = palette
        if cols4types:
            newdict = {}
            for k, v in cols4types.items():
                if not isinstance(k, tuple) or not len(k) == 2 or not isinstance(v, str):
                    raise Exception("cols4types: must be a dictionary mapping (setname,typename) to color string")
                newdict[k[0] + SEP + k[1]] = v
            parms["cols4types"] = newdict
        else:
            parms["cols4types"] = {}

        # Add the javascript
        jsloc = os.path.join(
            os.path.dirname(__file__), "ui_resources", JS_GATENLP_FILE_NAME
        )
        if not os.path.exists(jsloc):
            raise Exception(
                "Could not find JavsScript file, {} does not exist".format(
                    jsloc
                )
            )
        with open(jsloc, "rt", encoding="utf-8") as infp:
            js = infp.read()
            js = """<script type="text/javascript">""" + js + "</script>"

        if stretch_height:
            if row1_style is None:
                row1_style = gatenlpconfig.doc_html_repr_row1style_stretch
            if row2_style is None:
                row2_style = gatenlpconfig.doc_html_repr_row2style_stretch
        else:
            if row1_style is None:
                row1_style = gatenlpconfig.doc_html_repr_row1style_nostretch
            if row2_style is None:
                row2_style = gatenlpconfig.doc_html_repr_row2style_nostretch
        html = html.replace("$$JAVASCRIPT$$", js, 1).replace("$$JSONDATA$$", json, 1)
        html = html.replace("$$JSONPARMS$$", jsonlib.dumps(parms), 1)
        html = html.replace("$$ROW1STYLE$$", row1_style, 1).replace(
            "$$ROW2STYLE$$", row2_style, 1
        )
        if doc_style is None:
            doc_style = gatenlpconfig.doc_html_repr_doc_style
        if doc_style is None:
            doc_style = ""
        html = html.replace("$$DOCTEXTSTYLE$$", doc_style, 1)
        return html
