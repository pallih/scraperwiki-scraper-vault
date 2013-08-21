import scraperwiki
import urllib
import time
import re
from BeautifulSoup import BeautifulSoup

def valstr2int(s):
    return int(s.replace(" ", ""))

def error(entrylines, kapittel, post, overfraifjor, bevilgning, samlbevilgning, regnskap, rest):
    print entrylines
    raise ValueError("Missing value for kapittel " + kapittel + " post " + post)

def process_pdf(pdfurl):
# (harder example to work on: http://www.nihe.gov.uk/schemes_accepted_010109_to_310309.pdf )
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    s = BeautifulSoup(pdfxml)
    entrylines = []
    for text in s.findAll('text'):
        #print text
        entrylines.append(text)
        left = int(text['left'])
        if 82 == left:
            periode = text.text
            innut, m, y = periode.split(" ")
        if 107 == left:
            kapittel = text.text
        if 163 == left:
            post = text.text
        if 704 <= left and left <= 782:
            overfraifjor = text.text
        if 822 <= left and left <= 867:
            bevilgning = text.text
        if 920 <= left and left <= 965:
            samlbevilgning = text.text
        if 1011 <= left and left <= 1056:
            regnskap = text.text
        if 1124 <= left and left <= 1156 and u"1000 kr" != text.text.strip() and post is not None:
            rest = text.text
            if overfraifjor is None or bevilgning is None or samlbevilgning is None or regnskap is None or rest is None:
                error(entrylines, kapittel, post, overfraifjor, bevilgning, samlbevilgning, regnskap, rest)
            data = {
                'periode' : periode,
                'year' : y,
                'month' : m,
                'type' : innut,
                'kapittel' : kapittel,
                'post' : post,
                'overfraifjor' : valstr2int(overfraifjor),
                'bevilgning' : valstr2int(bevilgning),
                'samlbevilgning' : valstr2int(samlbevilgning),
                'regnskap' : valstr2int(regnskap),
                'rest' : valstr2int(rest),
            }
            #print data
            #time.sleep(1)
            scraperwiki.sqlite.save(unique_keys=['periode', 'kapittel', 'post'], data=data)
            post = None
            overfraifjor = None
            bevilgning = None
            samlbevilgning = None
            regnskap = None
            rest = None
            entrylines = []

process_pdf("http://www.sfso.no/upload/statsregnskapet/Maanedlig_statsregnskap/Oktober_2010/Statsregnskapet_utgifter_oktober_2010.pdf")
process_pdf("http://www.dfo.no/Documents/FOA/statsregnskapet/2010/november/Utgifter%20nov%202010.pdf")
process_pdf("http://www.dfo.no/Documents/FOA/statsregnskapet/2010/desember/Utgifter_2010.pdf")

# Found via http://www.dfo.no/no/Forvaltning/Statsregnskapet/Manedlig-statsregnskap/2012/, linked
# from http://www.dfo.no/no/Forvaltning/Statsregnskapet/Manedlig-statsregnskap/

process_pdf("http://www.dfo.no/Documents/FOA/statsregnskapet/2012/januar/Utgifter%20januar%202012.pdf")
process_pdf("http://www.dfo.no/Documents/FOA/statsregnskapet/2012/februar/Utgifter%20februar%202012.pdf")
process_pdf("http://www.dfo.no/Documents/FOA/statsregnskapet/2012/mars/Utgifter%20mars%202012.pdf")

#pdfurl = "https://www.bergen.kommune.no/bk/multimedia/archive/00090/Byr_dets_forslag_til_90384a.pdf"

