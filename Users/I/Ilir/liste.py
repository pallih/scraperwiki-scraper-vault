import scraperwiki
import requests
import sys
import os

from StringIO import StringIO
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import HTMLConverter, XMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.cmapdb import CMapDB
from bs4 import UnicodeDammit
from lxml.etree import tostring

import lxml.html


def find(root, tree, idx=0):
    if idx == len(tree):
        return root;
    node = tree[idx]
    if type(node) is dict:
        for k, v in node.iteritems():
            if root.attrib[k] != v:
                return None;
        return find(root, tree, idx+1)
    if type(node) is str: 
        arr = []
        for elem in root:
            if elem.tag == node:
                ret = find(elem, tree, idx+1)
                if ret is not None:
                    arr.append(ret)
    if len(arr) > 1:
        return arr
    if len(arr) == 1:
        return arr[0]
    return None


def read_pdf(url):
    pdf = requests.get(url);
    pdf_fp = StringIO(pdf.content)
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams(detect_vertical=True)
    device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
    
    process_pdf(rsrcmgr, device, pdf_fp, check_extractable=False)
    device.close()
    
    ret = retstr.getvalue()
    retstr.close()
    pdf_fp.close()
    return ret


def store_k(zupanija, grad_opcina, lista, kandidati):
    if not kandidati.startswith("http"):
        return
    doc = read_pdf(kandidati)
    scraperwiki.sqlite.save(unique_keys=["izvor"], data={"izvor": kandidati, "grad_opcina": grad_opcina, "lista": lista, "kandidati": doc}, table_name=zupanija)

def store_z(zupanija, lista, kandidati):
    if not kandidati.startswith("http"):
        return
    doc = read_pdf(kandidati)
    scraperwiki.sqlite.save(unique_keys=["izvor"], data={"izvor": kandidati, "grad_opcina": "", "lista": lista, "kandidati": doc}, table_name=zupanija)

startsection = "?" #start scraping from section
startsubsection = "?" #or start scraping from subsection
start = False #true if scraping all
    
if startsection == "*": #build city-county related table
    tables = scraperwiki.sqlite.show_tables()
    for table in tables:
        print table
        if table != "GRAD ZAGREB":
            #data = scraperwiki.sqlite.select('distinct lista from "' + table + '"')
            #for lista in data:
                #if lista['lista'].find("N.M.") > -1:
                    #print lista
            cities = scraperwiki.sqlite.select('distinct grad_opcina from "' + table + '"')
            for city in cities:
                grad_opcina = city['grad_opcina']
                if grad_opcina is not None:
                    scraperwiki.sqlite.save(unique_keys=["grad_opcina"], data={"grad_opcina": grad_opcina, "zupanija": table}, table_name="područja")

elif startsection == "!":
    scraperwiki.sqlite.execute("drop table if exists područja")
    scraperwiki.sqlite.commit()

sys.exit()

url = 'http://www.izbori.hr/2013Lokalni/kandid/'
html = scraperwiki.scrape(url + "index.html")
doc = UnicodeDammit(html, is_html=True)

parser = lxml.html.HTMLParser(encoding=doc.original_encoding)
root = lxml.html.document_fromstring(html, parser=parser)

data = find(root, ["body", "div", {"class": "main-table"}, "div", {"class": "data"}, "table", "tbody", "tr", "td", {"class": "acc-data"}])

for elem in data:
    header = find(elem, ["div", {"class": "acc-header"}])
    zupanija = header.text    
    if zupanija.startswith(startsection):
        start = True
    table = find(elem, ["div", {"class": "acc-body"}, "table"])
    if type(table) is list:
        st = find(table[0], ["tbody", "tr", "td", "a", "strong"])
        for s in st:
            if start:
                store_z(zupanija, s.text, url + s.getparent().attrib["href"])
        keys = [];
        values = [];
        thd = find(table[1], ["thead", "tr", "th"])
        for th in thd:
            if type(th) is list:
                for h in th:
                    keys.append(h.text)
            else:
                keys.append(th.text)
            
        idx = 0;
        cnt = len(keys)
        for i in range(0, cnt):
            values.append("")
        ttd = find(table[1], ["thead", "tr", "td"])
        if ttd is not None:
            for tr in ttd:
                for t in tr:
                    if t.text is not None and len(t.text) < 66:
#                        if start:
#                            print str(idx) + ":" + keys[idx] + ": " + t.text
                        values[idx] = t.text
                    elif len(t) > 0:
#                        if start:
#                            print str(idx) + ";" + keys[idx] + ": " + (url + t[0].attrib["href"])
                        values[idx] = url + t[0].attrib["href"]
                    if values[0].startswith(startsubsection):
                        start = True
                    idx = (idx + 1) % cnt;
                    if start and idx == 0:
                        for i in range(1, cnt):
                            store_k(zupanija, values[0], keys[i], values[i])
        tbd = find(table[1], ["tbody", "tr", "td"])
        if tbd is not None:
            for tr in tbd:
                if len(tr) == 0:
#                    if start:
#                        print str(idx) + " " + keys[idx] + ": " + tr.text
                    values[idx] = tr.text
                    idx = (idx + 1) % cnt                    
                    if start and idx == 0:
                        for i in range(1, cnt):
                            store_k(zupanija, values[0], keys[i], values[i])
                for t in tr:
                    if len(tr) == 1:
#                        if start:
#                            print str(idx) + " " + keys[idx] + ": " + (url + tr[0].attrib["href"])
                        values[idx] = url + tr[0].attrib["href"]
                    elif t.text is not None and len(t.text) < 66:
#                        if start:
#                            print str(idx) + " " + keys[idx] + ": " + t.text
                        values[idx] = t.text
                    elif len(t) > 0:
#                        if start:
#                            print str(idx) + " " + keys[idx] + ": " + (url + t[0].attrib["href"])
                        values[idx] = url + t[0].attrib["href"]
                    if values[0].startswith(startsubsection):
                        start = True
                    idx = (idx + 1) % cnt
                    if start and idx == 0:
                        for i in range(1, cnt):
                            store_k(zupanija, values[0], keys[i], values[i])
    else:
        st = find(table, ["tbody", "tr", "td", "a", "strong"])
        for s in st:
            store_z(zupanija, s.text, url + s.getparent().attrib["href"])

