from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import *
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed

filename = "test2.pdf"
def pdf2txt():
    filextension = filename.split('.')[-1].lower()
    if filextension == "pdf":
        pi = 0
        pdfout = StringIO()
        pdfrm = PDFResourceManager()
        converter = TextConverter(pdfrm, pdfout, laparams=LAParams())
        interpreter = PDFPageInterpreter(pdfrm, converter)
       
        infile = open(filename,'rb')
        for page in PDFPage.get_pages(infile):
            #仅检索前10页内容
            if pi > 9:
                break
            interpreter.process_page(page)
            pi += 1
        infile.close()
        converter.close()
        text = pdfout.getvalue()
        pdfout.close
    
    
    print(text[0:2000])
    
pdf2txt()