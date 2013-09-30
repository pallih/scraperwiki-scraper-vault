import scraperwiki
import lxml.html
import re

site = "http://www.defense.gov/contracts/contract.aspx?contractid=" 

def get_page_object(url):
    return lxml.html.fromstring( scraperwiki.scrape( url ) )

for contract in range(391, 4736):
    contract_link = get_page_object( '%s%s' % (site, contract) )
    contract_text = contract_link.text_content()
    contract = re.match( , contract_text)
import scraperwiki
import lxml.html
import re

site = "http://www.defense.gov/contracts/contract.aspx?contractid=" 

def get_page_object(url):
    return lxml.html.fromstring( scraperwiki.scrape( url ) )

for contract in range(391, 4736):
    contract_link = get_page_object( '%s%s' % (site, contract) )
    contract_text = contract_link.text_content()
    contract = re.match( , contract_text)
