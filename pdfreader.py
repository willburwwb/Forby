# -*- coding:utf-8 -*-
import os,re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams,LTTextBoxHorizontal,LTImage,LTCurve,LTFigure
from pdfminer.pdfpage import PDFTextExtractionNotAllowed,PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
fp=open(r"D:\file\HustLC\test\AI0.pdf","rb")
parser=PDFParser(fp)
document=PDFDocument(parser)
rsrcmgr=PDFResourceManager()
laparams=LAParams()
device=PDFPageAggregator(rsrcmgr,laparams=laparams)
interpreter=PDFPageInterpreter(rsrcmgr,device)
page_num=0
for page in PDFPage.create_pages(document):
    page_num=page_num+1
    interpreter.process_page(page)
    layout=device.get_result()
    for item in layout:
        line_count=0;
        if isinstance(item,LTTextBoxHorizontal):
            line=item.get_text().encode('utf-8')
            line_count=line_count+1
            match=re.search("a",str(line))
            if match:
                print("page:"+str(page_num)+"  content:"+str(line))

