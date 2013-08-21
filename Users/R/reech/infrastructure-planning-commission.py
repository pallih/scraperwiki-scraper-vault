from scraperwiki import scrape, datastore
from BeautifulSoup import BeautifulSoup
from lxml import etree
import urllib
import re
import json
import sys, traceback


# plenty of the data at this url is poorly/inconsistently formatted
list_url='http://infrastructure.independent.gov.uk/?page_id=202'
base_url='http://infrastructure.independent.gov.uk/'

# the data in the feed is no better structured
rss_url='http://mail.google.com/maps/ms?f=q&source=embed&hl=en&geocode=&ie=UTF8&hq=&hnear=Pembury,+Royal+Tunbridge+Wells,+Kent,+United+Kingdom&msa=0&output=georss&msid=116914771616832356584.00047840473f08d45f925'
rss_resource = etree.parse(urllib.urlopen(rss_url))
rss_resource = rss_resource.findall('//item')


def main():
    
    list_page = BeautifulSoup(scrape(list_url))
    list_tab  = list_page.find('table', {'id':'wp-table-reloaded-id-1-no-1'}).find('tbody')
    elements = list_tab.findAll('tr')
    print str(len(elements)) + ' applications'
    for e in elements:
        parse_row(e)

def fetch_location_details(applicant_name, location):
    # crudely match applicant and location against description
    l={'latlng':None ,}
    for r in rss_resource:
        e = r.getchildren()
        if e[3].text.find(applicant_name) > 0 and e[3].text.find(location) > 0: # crude string matching
            l['latlng'] =  e[5].text.strip().replace(' ',',')
            l['latlng'] = l['latlng'].split(',')
            l['latlng'] = (float(l['latlng'][0]), float(l['latlng'][1]))
            l['type'] = unicode(e[2].text.strip())
    return l

def formatExceptionInfo(maxTBlevel=5):
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)

def add_base(url):
    if re.match('^wp-content/.*',url):
        url = base_url + str(url)
    return unicode(url)

def parse_row(element):
    
    cell_names = ['location','proposal','applicant','contact_details','anticipated_date_of_application', 'scoping_document_urls']
    cells = element.findAll('td')
    application = dict(zip(cell_names, cells))
    
    # dates are inconsistently formatted
    application['anticipated_date_of_application']  = application['anticipated_date_of_application'].text.strip()
    
    a = re.match('^.*<a href="(.*?)".*',str(application['applicant']))
    if a:
        application['applicant_url'] = unicode(a.groups()[0])
    application['applicant'] = application['applicant'].text.strip()
    
    c = re.match('^.*<a href="mailto:(.*)".*',str(application['contact_details']))
    # contact details are inconsistently formatted
    if c:
        application['contact_email'] = unicode(c.groups()[0])
    application['contact_details'] = application['contact_details'].text.strip().replace('\uf',' ')
    # cr= re.match('^(.*)([(]{0,1}[0-9].*$)',application['contact_details'].text)
    # application['contact_name'] = cr.groups(0)
    application['proposal'] = application['proposal'].text.strip()
    application['location'] = application['location'].text.strip()
    application['scoping_document_urls'] = [sl['href'] for sl in application['scoping_document_urls'].findAll('a')]
    # print json.dumps(application['scoping_document_urls'], indent=4)
    application['scoping_document_urls'] = ','.join(map(add_base, application['scoping_document_urls']))
    l = fetch_location_details(application['applicant'], application['location'])
    application.update(l)
    coords = application['latlng']
    # print coords
    del(application['latlng'])
    # print application
    try:
        datastore.save(unique_keys=['applicant','location','proposal'], data=application, latlng=coords)
    except:
        print formatExceptionInfo()

main()