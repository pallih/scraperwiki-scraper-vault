import re
import uuid
import scraperwiki
import requests
import lxml.html as lh
import mechanize
from pprint import pprint

aspx_action = re.compile(r"javascript:__doPostBack\('(.+)',''\)")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2',
}

region_index_url = 'http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/lp_region_index'


selectors = {
    'firm_div': "//div[@id='main-column']/div[4]/div[2]/div[3]",
}

def get_page(url):
    r = session.get(url)
    return lh.fromstring(r.content)

def scrape_firm_page(response):
    data = {}

    firm_page = get_page(url)

    firm_div = firm_page.xpath(selectors['firm_div'])[0]

    title = firm_div.xpath("h3")[0].text_content().strip()
    
    headers = firm_div.xpath(".//td[@class='style1']")
    for h in headers:
        text = h.text_content().strip()
        text = text.rstrip(':').lower()
        if not text:
            continue
        filth = h.xpath("following-sibling::*[1]")[0].text_content().strip()
        if '\r\n' in filth:
            filth = [x.strip() for x in filth.split('\r\n')]
            filth = '\n'.join([x for x in filth if x])
        data[text] = filth
        
    data['firm_name'] = title

    return data

def follow_link(browser, link):
    print 'following', link.text
    href = link.attrib['href']
    # Extact the special action string from the uri
    black_magic = aspx_action.search(href).group(1)
    print 'special string:', repr(black_magic)
    browser.select_form(nr=0)
    browser.form.set_all_readonly(False)

    browser.form['__EVENTTARGET'] = black_magic
    browser.form['__EVENTARGUMENT'] = ''
    browser.form['lng'] = 'en-AU'
    browser.form['__VIEWSTATEENCRYPTED'] = ''
    browser.form['plc$lt$zoneHeader$SearchBox$txtWord'] = ''
    
    r = browser.submit()
    return r

def main():
    r = browser.open('http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/lp_firm_list&type=region&par1=K&'+str(uuid.uuid4()))
    tree = lh.fromstring(r.read())

    links = tree.xpath("//ol[1]/following-sibling::li/a")
    link = links[0]
    r = follow_link(browser, link)
    r = follow_link(browser, link)
    print browser.geturl()
    print r.read()
    #tree = lh.fromstring(r.read())
    
    
    #r = session.get('http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/lp_firm&id=206208')
    #data = scrape_firm_page(r)
    #data['region'] = region
    #pprint(data)

session = requests.session(headers=headers)
browser = mechanize.Browser()
browser.set_handle_equiv(True)
browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# Print HTTP headers.
#browser.set_debug_http(True)
browser.addheaders = headers.items()

main()
