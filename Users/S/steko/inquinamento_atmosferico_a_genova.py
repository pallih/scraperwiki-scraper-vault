###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import datetime
import dateutil.parser 

months = {
    'gennaio': '01',
    'febbraio': '02',
    'marzo': '03',
    'aprile': '04',
    'maggio': '05',
    'giugno': '06',
    'luglio': '07',
    'agosto': '08',
    'settembre': '09',
    'ottobre': '10',
    'novembre': '11',
    'dicembre': '12',
}

url = "http://www2.provincia.genova.it/datiaria/Tabulato.pdf"
#url = "http://steko.ominiverdi.org/aria/pdf/Tabulato_20111211.pdf"

pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

def getrealdata(el):
    return lxml.html.fromstring(gettext_with_bi_tags(el)).text_content()

data = {
    'station': 'Corso Buenos Aires',
    'measure': 'PM10',
    'unit': 'μg/m³',
    'timespan': datetime.timedelta(days=1),
    'value': None,
    }

# print the first hundred text elements from the first page
page0 = pages[0]
for el in list(page0):
    if el.tag == "text":
        if el.attrib['top'] == '210' and el.attrib['left'] == '481':
            datestring = getrealdata(el)
            datetuple = datestring.split()
            newdatestring = '%s-%s-%s' % (datetuple[2], months[datetuple[1]], datetuple[0])
            newdate = dateutil.parser.parse(newdatestring).date()
            data['date'] = newdate
        if el.attrib['top'] == '434':
            for n in range(794, 798):
                if el.attrib['left'] == str(n):
                    data['value'] = getrealdata(el)
            if int(el.attrib['left']) + int(el.attrib['width']) >= 818:
                temp = getrealdata(el)
                templs = temp.split()
                data['value'] = templs[-1]

if data['value'] is not None:
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)

