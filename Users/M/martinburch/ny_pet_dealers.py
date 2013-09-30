#http://www.agriculture.ny.gov/petdealer/petdealerextract.asp

import scraperwiki
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import urllib2

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `inspections` (`inspdate` text, `rating` text, `area` text, `licno` text, `detailurl` text, `resulttype` text, `corp` text, `pdf` text)")

def scrape_pdf(soup_pdf):
    tds = soup_pdf.findAll('text') # get all the <text> tags
    tds_text = [None]*len(tds)
    for i in range(len(tds)): #changing tags to the text within the tag
        tds_text[i] = tds[i].text
    data = {}

    data['rating'] = tds_text[tds_text.index('Purpose:') + 5]
    # If we didn't get anything useful, try a different index
    if (data['rating'] == "Inspection"):
        data['rating'] = tds_text[tds_text.index('Purpose:') + 4]    
    
    data['resulttype'] = data['rating'].split(' ')[0]
    return data

#for testing, use http://dl.dropbox.com/u/58785631/pet-dealer-scraper/petdealerextract.asp.html


doc = urllib2.urlopen("http://www.agriculture.ny.gov/petdealer/petdealerextract.asp").read()
links = SoupStrainer('a', href=re.compile(r'^Pet'))

for el in BeautifulSoup(doc, parseOnlyThese=links):
    suburl = 'http://www.agriculture.ny.gov/petdealer/'+urllib2.quote(el["href"], '?=&')
    subdoc = urllib2.urlopen(suburl).read()
    sublinks = SoupStrainer('a', href=re.compile(r'^Insp'))
    print el["href"]
    corp = el["href"].partition('?')[2].partition('&')[2].split('=')[1].split(' - ')[1]
    area = el["href"].partition('?')[2].partition('&')[2].split('=')[1].split(' - ')[0]
    for subel in BeautifulSoup(subdoc, parseOnlyThese=sublinks):
        print subel["href"]
        # splitting on backslash, must escape
        licno = subel["href"].split("\\")[1].split('__')[0]
        date = subel["href"].split("\\")[1].split('__')[1].split('.')[0]
        a = scraperwiki.scrape("http://www.agriculture.ny.gov/petdealer/"+subel["href"])
        soup_pdf = BeautifulSoup(scraperwiki.pdftoxml(a))
        data = scrape_pdf(soup_pdf)

#TODO: Replace save() statement with standard SQL
#https://scraperwiki.com/docs/python/python_datastore_guide/

        scraperwiki.sqlite.save(unique_keys=["pdf"],data={"detailurl":el["href"], "pdf":subel["href"], "rating":data['rating'], "corp":corp, "area":area,"licno":licno,"inspdate":date,"resulttype":data['resulttype']},table_name="inspections")
#http://www.agriculture.ny.gov/petdealer/petdealerextract.asp

import scraperwiki
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import urllib2

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `inspections` (`inspdate` text, `rating` text, `area` text, `licno` text, `detailurl` text, `resulttype` text, `corp` text, `pdf` text)")

def scrape_pdf(soup_pdf):
    tds = soup_pdf.findAll('text') # get all the <text> tags
    tds_text = [None]*len(tds)
    for i in range(len(tds)): #changing tags to the text within the tag
        tds_text[i] = tds[i].text
    data = {}

    data['rating'] = tds_text[tds_text.index('Purpose:') + 5]
    # If we didn't get anything useful, try a different index
    if (data['rating'] == "Inspection"):
        data['rating'] = tds_text[tds_text.index('Purpose:') + 4]    
    
    data['resulttype'] = data['rating'].split(' ')[0]
    return data

#for testing, use http://dl.dropbox.com/u/58785631/pet-dealer-scraper/petdealerextract.asp.html


doc = urllib2.urlopen("http://www.agriculture.ny.gov/petdealer/petdealerextract.asp").read()
links = SoupStrainer('a', href=re.compile(r'^Pet'))

for el in BeautifulSoup(doc, parseOnlyThese=links):
    suburl = 'http://www.agriculture.ny.gov/petdealer/'+urllib2.quote(el["href"], '?=&')
    subdoc = urllib2.urlopen(suburl).read()
    sublinks = SoupStrainer('a', href=re.compile(r'^Insp'))
    print el["href"]
    corp = el["href"].partition('?')[2].partition('&')[2].split('=')[1].split(' - ')[1]
    area = el["href"].partition('?')[2].partition('&')[2].split('=')[1].split(' - ')[0]
    for subel in BeautifulSoup(subdoc, parseOnlyThese=sublinks):
        print subel["href"]
        # splitting on backslash, must escape
        licno = subel["href"].split("\\")[1].split('__')[0]
        date = subel["href"].split("\\")[1].split('__')[1].split('.')[0]
        a = scraperwiki.scrape("http://www.agriculture.ny.gov/petdealer/"+subel["href"])
        soup_pdf = BeautifulSoup(scraperwiki.pdftoxml(a))
        data = scrape_pdf(soup_pdf)

#TODO: Replace save() statement with standard SQL
#https://scraperwiki.com/docs/python/python_datastore_guide/

        scraperwiki.sqlite.save(unique_keys=["pdf"],data={"detailurl":el["href"], "pdf":subel["href"], "rating":data['rating'], "corp":corp, "area":area,"licno":licno,"inspdate":date,"resulttype":data['resulttype']},table_name="inspections")
