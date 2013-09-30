import scraperwiki
from lxml.html import tostring, fromstring

base_url = 'http://www.lbhf.gov.uk/Community_Service_Directory/'

def get_services(category, trs):
    for tr in trs:
        print tostring(tr)
        tds = tr.cssselect("td")
    
        if len(tds) == 0:
            continue
        ahref = tds[0].cssselect("a")[0]
        link = ahref.attrib["href"]
        if category == 'Community Services':
            id = link.split('_')[0]
        elif category == 'Family Services':
            id = link.replace('result_detail.asp?externalId=', '')
        title = ahref.text_content()
        sub_category = tds[1].text_content()
        telephone_number = tds[2].text_content()
    
        print title, sub_category, telephone_number, link
    
        data = {
            'id' : id,
            'link' : base_url + link,
            'title' : title,
            'category' : category,
            'sub_category' : sub_category,
            'telephone_number' : telephone_number,
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def run_scraper():
    html = scraperwiki.scrape(base_url + 'Results.asp?Go=Select')
    root = fromstring(html)
    tables = root.cssselect("table#events_results")
    
    trs = tables[0].cssselect("tr")
    get_services('Community Services', trs)
    trs = tables[1].cssselect("tr")
    get_services('Family Services', trs)

run_scraper()

import scraperwiki
from lxml.html import tostring, fromstring

base_url = 'http://www.lbhf.gov.uk/Community_Service_Directory/'

def get_services(category, trs):
    for tr in trs:
        print tostring(tr)
        tds = tr.cssselect("td")
    
        if len(tds) == 0:
            continue
        ahref = tds[0].cssselect("a")[0]
        link = ahref.attrib["href"]
        if category == 'Community Services':
            id = link.split('_')[0]
        elif category == 'Family Services':
            id = link.replace('result_detail.asp?externalId=', '')
        title = ahref.text_content()
        sub_category = tds[1].text_content()
        telephone_number = tds[2].text_content()
    
        print title, sub_category, telephone_number, link
    
        data = {
            'id' : id,
            'link' : base_url + link,
            'title' : title,
            'category' : category,
            'sub_category' : sub_category,
            'telephone_number' : telephone_number,
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def run_scraper():
    html = scraperwiki.scrape(base_url + 'Results.asp?Go=Select')
    root = fromstring(html)
    tables = root.cssselect("table#events_results")
    
    trs = tables[0].cssselect("tr")
    get_services('Community Services', trs)
    trs = tables[1].cssselect("tr")
    get_services('Family Services', trs)

run_scraper()

