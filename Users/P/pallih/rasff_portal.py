import scraperwiki
import requests
import lxml.html
import re
from lxml import etree

#scraperwiki.sqlite.save_var('last_nr', '2101') 

#exit()

xml = 'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=searchResultXML&StartRow=0'

last_done = scraperwiki.sqlite.get_var('last_nr')

regex = re.compile(".*Row=(\d.*)")

result_xpath = '//tr'

pick_up_cookies_url = 'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=searchResultList'

start_url = 'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=searchResultList&StartRow=' + last_done

next_page_xpath = '//table[@width="100%"]/tr/td[2]/a[contains(text(),"Next")]'

def get_results(result_url):
    done = regex.search(result_url)
    scraperwiki.sqlite.save_var('last_nr', done.groups()[0])
    r = s.get(result_url, verify=False) # set verify to false to bypass the SSL cert
    process(r.text)
    root = lxml.html.fromstring(r.text)
    next_page_table = root.xpath(next_page_xpath)
    for x in next_page_table:
        if x.attrib['href']:
            get_results(x.attrib['href'])
        else:
            print
            print 'DONE'

def process(html):

    root = lxml.html.fromstring(html)

    trs = root.xpath(result_xpath)

    for tr in trs[3:]:
        record = {}
        record['classification'] = tr[1].text_content().strip()
        record['date_of_case'] = tr[2].text_content().strip()
        record['last_change'] = tr[3].text_content().strip()
        record['detail_url'] = tr[4][0].attrib['href']
        record['reference'] = tr[4].text_content().strip()
        record['country'] = tr[5].text_content().strip()
        record['subject'] = tr[6].text_content().strip()
        try:
            record['category'] = tr[7].text_content().strip()
        

            record['type'] = tr[8].text_content().strip()
        except:
            pass 
        scraperwiki.sqlite.save(unique_keys=['reference'], data=record, verbose=1)

s = requests.session()

s.get(pick_up_cookies_url, verify=False)

get_results(start_url)







import scraperwiki
import requests
import lxml.html
import re
from lxml import etree

#scraperwiki.sqlite.save_var('last_nr', '2101') 

#exit()

xml = 'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=searchResultXML&StartRow=0'

last_done = scraperwiki.sqlite.get_var('last_nr')

regex = re.compile(".*Row=(\d.*)")

result_xpath = '//tr'

pick_up_cookies_url = 'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=searchResultList'

start_url = 'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=searchResultList&StartRow=' + last_done

next_page_xpath = '//table[@width="100%"]/tr/td[2]/a[contains(text(),"Next")]'

def get_results(result_url):
    done = regex.search(result_url)
    scraperwiki.sqlite.save_var('last_nr', done.groups()[0])
    r = s.get(result_url, verify=False) # set verify to false to bypass the SSL cert
    process(r.text)
    root = lxml.html.fromstring(r.text)
    next_page_table = root.xpath(next_page_xpath)
    for x in next_page_table:
        if x.attrib['href']:
            get_results(x.attrib['href'])
        else:
            print
            print 'DONE'

def process(html):

    root = lxml.html.fromstring(html)

    trs = root.xpath(result_xpath)

    for tr in trs[3:]:
        record = {}
        record['classification'] = tr[1].text_content().strip()
        record['date_of_case'] = tr[2].text_content().strip()
        record['last_change'] = tr[3].text_content().strip()
        record['detail_url'] = tr[4][0].attrib['href']
        record['reference'] = tr[4].text_content().strip()
        record['country'] = tr[5].text_content().strip()
        record['subject'] = tr[6].text_content().strip()
        try:
            record['category'] = tr[7].text_content().strip()
        

            record['type'] = tr[8].text_content().strip()
        except:
            pass 
        scraperwiki.sqlite.save(unique_keys=['reference'], data=record, verbose=1)

s = requests.session()

s.get(pick_up_cookies_url, verify=False)

get_results(start_url)







