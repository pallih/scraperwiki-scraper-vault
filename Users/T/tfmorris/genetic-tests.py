import scraperwiki
import lxml.html
from datetime import datetime

sites = [('Gendx','http://www.genedx.com/test-catalog/available-tests/','div#catalog-content ul li a.main'),
        ('Ambrygen','http://www.ambrygen.com/tests-by-gene','td.views-field-field-tests a'),
        ('BCM','http://www.bcm.edu/geneticlabs/tests.cfm','div#content div a'),
        ]

def process_test(site,name,url):
    #print 'Processing %s at %s' % (name, url)
    rec = {'date_scraped' : datetime.now(),
           'site':site,
           'test_name':name,
           'genes':[],
           'icd_codes':[],
           'price': 0.0
           }
    scraperwiki.sqlite.save(['site','test_name'], rec)
    pass

def main():
    for site,url,test_selector in sites:
        print 'Processing site %s at %s' % (site, url)
        index_html = scraperwiki.scrape(url)
        index = lxml.html.fromstring(index_html)
        tests = index.cssselect(test_selector)
        # TODO eliminate duplicate listings (e.g. tests listed under multiple genes)
        print 'found %d total test listings' % len(tests)
        for test in tests:
            name = test.text_content()
            page_url = test.attrib['href']
            # TODO canonicalize URLs
            process_test(site,name,page_url)

main()import scraperwiki
import lxml.html
from datetime import datetime

sites = [('Gendx','http://www.genedx.com/test-catalog/available-tests/','div#catalog-content ul li a.main'),
        ('Ambrygen','http://www.ambrygen.com/tests-by-gene','td.views-field-field-tests a'),
        ('BCM','http://www.bcm.edu/geneticlabs/tests.cfm','div#content div a'),
        ]

def process_test(site,name,url):
    #print 'Processing %s at %s' % (name, url)
    rec = {'date_scraped' : datetime.now(),
           'site':site,
           'test_name':name,
           'genes':[],
           'icd_codes':[],
           'price': 0.0
           }
    scraperwiki.sqlite.save(['site','test_name'], rec)
    pass

def main():
    for site,url,test_selector in sites:
        print 'Processing site %s at %s' % (site, url)
        index_html = scraperwiki.scrape(url)
        index = lxml.html.fromstring(index_html)
        tests = index.cssselect(test_selector)
        # TODO eliminate duplicate listings (e.g. tests listed under multiple genes)
        print 'found %d total test listings' % len(tests)
        for test in tests:
            name = test.text_content()
            page_url = test.attrib['href']
            # TODO canonicalize URLs
            process_test(site,name,page_url)

main()