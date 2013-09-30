import scraperwiki
from lxml import etree, html
import time

#utf-8 Parser required to correctly interprete data 
parser = etree.HTMLParser(encoding = "utf-8")

#Determine the links to the lists of each type of legislation 
page = html.parse("http://www.legislation.gov.uk/browse", parser = parser)
doc_types = [x.attrib["href"] for x in page.findall('//body//ul[@class="legTypes"]//li//a')]
#doc_types.remove("/ukla")
#doc_types.remove("/ukpga")
#doc_types.remove("/uksi")
#doc_types.remove("/asp")
#doc_types.remove("/wsi")
#doc_types.remove("/ssi")
#doc_types.remove("/nisr")

attempts = 0 #Counter of number of attempts that have been made to get a document
for doc_type in doc_types:
    page_number = 1
    while True:
        starting_url = 'http://www.legislation.gov.uk%s?page=%i' % (doc_type, page_number)
        try:
            page = html.parse(starting_url, parser = parser)
            #Determine if page_number is the one returned
            correct_page = False
            results_page = False
            for text in [html.tostring(x) for x in page.findall("//body//strong")]:
                correct_page = correct_page or ("This is results page" in text and str(page_number) in text)
                results_page = results_page or "This is results page" in text
            if not results_page: #This means that the wrong data was loaded
                raise AsertionError
            if not correct_page:
                #This probably means that we have got to the last page
                break
            #Look though the tables in the document
            tables = page.findall('//table')
            for table in tables:
                if not(table.attrib.has_key('class')) or table.attrib["class"] != 'decades':
                    trs = table.findall('tbody//tr')
                    for tr in trs:
                        tds = list(tr.findall('td'))
                        if len(tds) == 3:
                            record = {"title": tds[0].find("a").text,
                                      "link": tds[0].find("a").attrib["href"],
                                      "year_number": tds[1].find("a").text,
                                      "legislation_type": tds[2].text}
                            scraperwiki.datastore.save(["title", "year_number"], record)
        except (IOError, AssertionError):
            attempts = attempts + 1
            if attempts == 5:
                print "Failed to get %s page %i" % (doc_type, page_number)  
                break
            time.sleep(300)
            continue
        page_number = page_number + 1
        attempts = 0 #Counter of number of attempts that have been made to get a document
import scraperwiki
from lxml import etree, html
import time

#utf-8 Parser required to correctly interprete data 
parser = etree.HTMLParser(encoding = "utf-8")

#Determine the links to the lists of each type of legislation 
page = html.parse("http://www.legislation.gov.uk/browse", parser = parser)
doc_types = [x.attrib["href"] for x in page.findall('//body//ul[@class="legTypes"]//li//a')]
#doc_types.remove("/ukla")
#doc_types.remove("/ukpga")
#doc_types.remove("/uksi")
#doc_types.remove("/asp")
#doc_types.remove("/wsi")
#doc_types.remove("/ssi")
#doc_types.remove("/nisr")

attempts = 0 #Counter of number of attempts that have been made to get a document
for doc_type in doc_types:
    page_number = 1
    while True:
        starting_url = 'http://www.legislation.gov.uk%s?page=%i' % (doc_type, page_number)
        try:
            page = html.parse(starting_url, parser = parser)
            #Determine if page_number is the one returned
            correct_page = False
            results_page = False
            for text in [html.tostring(x) for x in page.findall("//body//strong")]:
                correct_page = correct_page or ("This is results page" in text and str(page_number) in text)
                results_page = results_page or "This is results page" in text
            if not results_page: #This means that the wrong data was loaded
                raise AsertionError
            if not correct_page:
                #This probably means that we have got to the last page
                break
            #Look though the tables in the document
            tables = page.findall('//table')
            for table in tables:
                if not(table.attrib.has_key('class')) or table.attrib["class"] != 'decades':
                    trs = table.findall('tbody//tr')
                    for tr in trs:
                        tds = list(tr.findall('td'))
                        if len(tds) == 3:
                            record = {"title": tds[0].find("a").text,
                                      "link": tds[0].find("a").attrib["href"],
                                      "year_number": tds[1].find("a").text,
                                      "legislation_type": tds[2].text}
                            scraperwiki.datastore.save(["title", "year_number"], record)
        except (IOError, AssertionError):
            attempts = attempts + 1
            if attempts == 5:
                print "Failed to get %s page %i" % (doc_type, page_number)  
                break
            time.sleep(300)
            continue
        page_number = page_number + 1
        attempts = 0 #Counter of number of attempts that have been made to get a document
