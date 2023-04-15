from gatenlp import Document


class TestGate:
    def __init__(self):

        text = """Barack Obama was the 44th president of the US and he followed George W. Bush and
          was followed by Donald Trump. Before Bush, Bill Clinton was president.
          Also, lets include a sentence about South Korea which is called 대한민국 in Korean.
          And a sentence with the full name of Iran in Farsi: جمهوری اسلامی ایران and also with 
          just the word "Iran" in Farsi: ایران 
          Also barack obama in all lower case and SOUTH KOREA in all upper case
          """
        doc = Document(text)

        # set a document feature
        doc.features["purpose"] = "simple illustration of gatenlp basics"

        # get the default annotation set
        defset = doc.annset()

        # add an annotation that spans the whole document, no features
        defset.add(0, len(doc), "Document", {})

        print(defset)
