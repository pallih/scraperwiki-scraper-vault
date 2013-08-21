###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import lxml.html
from lxml import etree
import re

def extract_text(html):
    trs = html.xpath("//*[@id='CompanylistResults']//tr[td[not(@class='quick-links' or @colspan='6')]]")
    for tr in trs:
        tds = tr.cssselect("td")
        homepagelist =  tds[0].xpath("a/@href")
        homepage = '' 
        if len(homepagelist) > 0: homepage = homepagelist[0]
        symbollist = tds[1].xpath(".//div[@class='symbol_links']//h3//a/text()")
        symbol =  symbollist[0].strip()                
        #print homepage + '|' + tds[0].text_content().strip() + '|' + symbol + '|' + tds[2].text_content() + '|' + tds[3].text_content() + '|' + tds[4].text_content() + '|' + tds[5].text_content() + '|' + tds[6].text_content()  
        #print '|'.join(td.text_content().strip() for td in tds )
        #Name     Symbol     Market Value     Country     IPO Year     Subsector
        record = {}
        record['homepage'] = homepage
        record['name'] = tds[0].text_content().strip()
        record['symbol'] = symbol
        record['marketvalue'] =  tds[2].text_content()
        record['country'] =  tds[3].text_content()
        record['ipoyear'] =  tds[4].text_content()
        record['sector'] =  tds[5].text_content()
        scraperwiki.datastore.save(["symbol"], record)



base_url = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?industry=Technology&pagesize=200&page='
starting_url = base_url + '1'


root = lxml.html.parse(starting_url)
extract_text(root)
noofpageshref = root.xpath("//ul[@class='pager']//li[a/text()='last >>']//a/@href")[0].strip()


rg = re.compile('page=([0-9]+)',re.IGNORECASE|re.DOTALL)
m = rg.search(noofpageshref)
noofpages = int(m.group(1))

for pg in range(2,noofpages+1):
    root = lxml.html.parse(base_url + `pg`)
    extract_text(root)  


    