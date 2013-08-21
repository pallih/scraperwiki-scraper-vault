import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO



def scrape(content): #Parse the javascript geodata and store in database
    clean_content = content[3079:] #Yes, this is very naughty.
    projects_list = clean_content.split("},{")
    for project in projects_list:
        doc = etree.parse(StringIO(project), parser=etree.HTMLParser())
        data = {}
        coordinates= []
        coordinates= re.findall(r'\(([0-9.-]+).+?([0-9.-]+)', project)
        data['coordinates']= coordinates[0]
        core_url = 'http://www.povertyactionlab.org'
        clean_url = core_url + str(doc.find("//a").attrib["href"].replace('\\',''))
        data['url'] = clean_url.replace('"','')
        data['title'] = doc.xpath("//div[contains(@class, 'popup-title')]/a/text()")[0]
        #data['authors'] = doc.xpath("//div[contains(@class, 'popup-name')]/text()") #Coudn't get authors to work due to inconsitent <a> tag usage
        data['abstract'] = doc.xpath("//span[contains(@class, 'views-field-teaser')]/text()")[0]
        scraperwiki.sqlite.save(["title"], data) #Store data in sqlite database


def JPAL_data_prep(content):#function to grab geodata from JPAL javascript
    records = []
    doc = etree.parse(StringIO(content), parser=etree.HTMLParser())
    preped_data = doc.xpath('/html/head/script[22]/text()')[0]
    return scrape(preped_data)


def JPAL_load(): #function to scrape JPAL page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request("http://www.povertyactionlab.org/search/apachesolr_search?view=map&filters=type:evaluation", "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return JPAL_data_prep(content)



JPAL_load()


