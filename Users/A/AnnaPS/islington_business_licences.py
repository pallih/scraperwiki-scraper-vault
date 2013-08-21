from BeautifulSoup import BeautifulSoup
from datetime import datetime
import lxml
from lxml.html import fromstring
from xml.dom import minidom 
import mechanize
import scraperwiki
try: import simplejson as json
except ImportError: import json
import urllib2
from urlparse import urlparse

# Load our existing records, so we can persist date_scraped between runs. 
DATA_URL = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=islington_business_licences&query=select%20*%20from%20swdata&limit%20100000'
existing_records = urllib2.urlopen(DATA_URL).read()
existing_records = json.loads(existing_records)

def get_next_link(browser):
    for link in browser.links():
        if link.text=='Go to next page[IMG]':
            return link
    return None

def scrape_page(page_url, licence_name):
    print page_url
    response = br.open(page_url)
    param = page_url.split("?")[1].split("&")
    id = param[2].replace('PARAM0=','').replace("'","")
    soup = BeautifulSoup(response.read()) # lxml can't cope with this HTML, use BeautifulSoup. 
    ul = soup.find("ul", { "class" : "list" })
    lis = ul.findAll("div")
    data = {}
    data['licence_type'] = licence_name
    data['id'] = id
    match_found = False
    for x in existing_records:
        if x['id']==data['id']:#
            scraperwiki.sqlite.save(['id'], x) 
            match_found = True
            return False
    match_found = False
    if not match_found:
        data['date_scraped'] = datetime.now()
        data['url'] = page_url
        for i, li in enumerate(lis):
            title = li.find('span')
            val = li.renderContents().replace(str(title),"").strip()
            #val = unicode(val).replace(u'\xc2', u'').replace(u'\xa0', u'')
            title = title.renderContents().strip()
            def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
            data[title.lower().replace(" ","_")] = removeNonAscii(val)
        scraperwiki.sqlite.save(['id'], data)
        return True

def scrape_list_of_results(htmlstring, next_link, licence_name):
    doc = fromstring(htmlstring)
    # Scrape each link
    for i, tr in enumerate(doc.cssselect('table.display_table tr')):
        if i==0: continue
        licence_link = DOMAIN + 'Northgate/Online/EGov/License_Registers/' + tr.cssselect('a.data_text')[0].attrib['href']
        ''.join(licence_link.split())
        licence_link = licence_link.replace('\r','').replace('\t','').replace('\n','').replace(" ","")
        #print licence_link
        scrape_page(licence_link, licence_name)
    if next_link:
        nextresponse = br.follow_link(next_link)
        next_link = get_next_link(br)
        scrape_list_of_results(nextresponse.read(), next_link, licence_name)

DOMAIN = 'http://www.islington.gov.uk/'
LICENCE_URL = DOMAIN + 'Northgate/Online/EGov/License_Registers/Registers_Criteria.aspx'
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
j=0

licence_types = {"LTEN":"Temporary Event Notice","LPRE":"Premises Licence"}
for acronym,licence_name in licence_types.items():
    br.open(LICENCE_URL)
    br.select_form(nr=0)
    control = br.form.find_control("ddLiceType")
    control.value = [acronym]
    response = br.open(br.click())
    next_link = get_next_link(br)
    scrape_list_of_results(response.read(), next_link, licence_name)

