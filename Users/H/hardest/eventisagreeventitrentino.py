import scraperwiki
import lxml.html
import re

DEFAULT_ANY23_PAGE = '<http://any23.org/tmp/>' 

BASE_URL = 'http://www.eventiesagre.it/'

FIRST_RESULT_PAGE = BASE_URL + 'cerca/cat/sez/mesi/Trentino%20Alto%20Adige/prov/cit/intit/rilib'

def process_info(page_url, info):
    info_parts = info.replace('<td>', '').replace('</td>', '').split('<br>')
    description = ''
    triples = ''
    tel_re = re.compile('(\+?[\s?\(?\)?\d]+)')
    for info_part in info_parts:
        phone = max(tel_re.findall(info_part), key=len) 
        if len( phone.strip() ) == 0 : continue
        phone = re.sub('[A-Za-z\s\.]', '', phone)
        triples += '<{0}> vcard:phone "{1}".\n'.format(page_url, phone)
    return triples

def process_page(page_url):
    print 'Processing page', page_url
    page_html = scraperwiki.scrape(page_url)
    page_rdf  = scraperwiki.scrape('http://any23.org/any23', {'type' : 'text/html', 'format' : 'turtle', 'body' : page_html})
    page_dom  = lxml.html.fromstring(page_html)    
    
    info    = None
    email   = None
    website = None
    try:
        info = lxml.html.tostring( page_dom.cssselect('img[alt="info evento"]')[0].getparent().getnext() )
        print "PROCESS_INFO", process_info(page_url, info)
    except BaseException as e: print 'Info not found.', e
    try: 
        email = page_dom.cssselect('img[alt="e-mail"]')[0].getnext().text_content() 
    except BaseException as e: print 'EMail not found.', e
    try: 
        website = page_dom.cssselect('img[alt="Sito Web Esterno"]')[0].getnext().get('href') 
    except BaseException as e: print 'Website not found.', e
            
    if email:   
        page_rdf += '<{0}> vcard:email "{1}".\n'.format(page_url, email)
    if website: 
        page_rdf += '<{0}> vcard:url   "{1}".\n'.format(page_url, website)
    
    page_rdf = page_rdf.replace(DEFAULT_ANY23_PAGE, '<{0}>'.format(page_url))
    data = {
        'url'    : page_url,
        'turtle' : page_rdf
    }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    

def process_result_page(result_page):
    result_page_html = scraperwiki.scrape(result_page)
    result_page_dom  = lxml.html.fromstring(result_page_html)
    for detail_page_link in result_page_dom.cssselect('a.summary'):
        process_page( BASE_URL + detail_page_link.get('href') )
    
    try:
        for next_pagination_url in result_page_dom.cssselect('tr.elencoNav a'):        
            if next_pagination_url.text_content().strip().lower() == 'avanti':
                process_result_page( next_pagination_url.get('href') )
                break
            else:
                print 'No more pages.'
    except BaseException as e:
        print 'Error while processing pagination', e        


process_result_page(FIRST_RESULT_PAGE)

import scraperwiki
import lxml.html
import re

DEFAULT_ANY23_PAGE = '<http://any23.org/tmp/>' 

BASE_URL = 'http://www.eventiesagre.it/'

FIRST_RESULT_PAGE = BASE_URL + 'cerca/cat/sez/mesi/Trentino%20Alto%20Adige/prov/cit/intit/rilib'

def process_info(page_url, info):
    info_parts = info.replace('<td>', '').replace('</td>', '').split('<br>')
    description = ''
    triples = ''
    tel_re = re.compile('(\+?[\s?\(?\)?\d]+)')
    for info_part in info_parts:
        phone = max(tel_re.findall(info_part), key=len) 
        if len( phone.strip() ) == 0 : continue
        phone = re.sub('[A-Za-z\s\.]', '', phone)
        triples += '<{0}> vcard:phone "{1}".\n'.format(page_url, phone)
    return triples

def process_page(page_url):
    print 'Processing page', page_url
    page_html = scraperwiki.scrape(page_url)
    page_rdf  = scraperwiki.scrape('http://any23.org/any23', {'type' : 'text/html', 'format' : 'turtle', 'body' : page_html})
    page_dom  = lxml.html.fromstring(page_html)    
    
    info    = None
    email   = None
    website = None
    try:
        info = lxml.html.tostring( page_dom.cssselect('img[alt="info evento"]')[0].getparent().getnext() )
        print "PROCESS_INFO", process_info(page_url, info)
    except BaseException as e: print 'Info not found.', e
    try: 
        email = page_dom.cssselect('img[alt="e-mail"]')[0].getnext().text_content() 
    except BaseException as e: print 'EMail not found.', e
    try: 
        website = page_dom.cssselect('img[alt="Sito Web Esterno"]')[0].getnext().get('href') 
    except BaseException as e: print 'Website not found.', e
            
    if email:   
        page_rdf += '<{0}> vcard:email "{1}".\n'.format(page_url, email)
    if website: 
        page_rdf += '<{0}> vcard:url   "{1}".\n'.format(page_url, website)
    
    page_rdf = page_rdf.replace(DEFAULT_ANY23_PAGE, '<{0}>'.format(page_url))
    data = {
        'url'    : page_url,
        'turtle' : page_rdf
    }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    

def process_result_page(result_page):
    result_page_html = scraperwiki.scrape(result_page)
    result_page_dom  = lxml.html.fromstring(result_page_html)
    for detail_page_link in result_page_dom.cssselect('a.summary'):
        process_page( BASE_URL + detail_page_link.get('href') )
    
    try:
        for next_pagination_url in result_page_dom.cssselect('tr.elencoNav a'):        
            if next_pagination_url.text_content().strip().lower() == 'avanti':
                process_result_page( next_pagination_url.get('href') )
                break
            else:
                print 'No more pages.'
    except BaseException as e:
        print 'Error while processing pagination', e        


process_result_page(FIRST_RESULT_PAGE)

