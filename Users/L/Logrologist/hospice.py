import scraperwiki
import lxml.html
import re
from lxml.html.clean import Cleaner
from lxml import etree

print "I'm running!"

html = "http://www.nahcagencylocator.com/SearchResult.asp?rad=ALL&rad3=&city=&state=CA&ftype=&map=yes"
cleaner = Cleaner(page_structure=False, links=False)
html_page = scraperwiki.scrape(html)

splitter = html_page.split('<div class="listNav">')
print splitter[1]
splatter = splitter[1].split('"><img src="')
print splatter[0]
splotter = splatter[0].split('><a href="')
print splotter[1]



page_count=1
max_page = 2  # actual max_page count is 96  
address_count=1

while page_count < max_page:
    # html_new = "http://www.nahcagencylocator.com/"
    html_page = scraperwiki.scrape(html)
    
    root = lxml.html.fromstring(html_page)
    r = root.cssselect('div.contactCard')
    # print r[0].text_content()
    for x in r:
        trs = x.cssselect("tr")
        tds = x.cssselect("td")
        for y in trs:
            if address_count < 8:
                data = { 'address': tds[1].text_content() }
                print "kerblaawww!!!"
                print tds[1].text_content()
                # print data
                keep_data = data['address']
                # arr_data = keep_data.split(' ')
                print keep_data
                # print arr_data
                final_data = {'name': '', 'address': '', 'address_2': '', 'city': '', 'state': 'CA', 'zip': 00000, 'phone': 555-555-5555, 'fax': 5}
                scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address_count, "bbb":keep_data})
                address_count+=1
            else:
                data = { 'address': tds[0].text_content() }
                keep_data = data['address']
                print data['address']
                scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address_count, "bbb":keep_data})
                address_count+=1

    page_count+=1
    
    
    print page_count   

print "END OF DOCUMENT"import scraperwiki
import lxml.html
import re
from lxml.html.clean import Cleaner
from lxml import etree

print "I'm running!"

html = "http://www.nahcagencylocator.com/SearchResult.asp?rad=ALL&rad3=&city=&state=CA&ftype=&map=yes"
cleaner = Cleaner(page_structure=False, links=False)
html_page = scraperwiki.scrape(html)

splitter = html_page.split('<div class="listNav">')
print splitter[1]
splatter = splitter[1].split('"><img src="')
print splatter[0]
splotter = splatter[0].split('><a href="')
print splotter[1]



page_count=1
max_page = 2  # actual max_page count is 96  
address_count=1

while page_count < max_page:
    # html_new = "http://www.nahcagencylocator.com/"
    html_page = scraperwiki.scrape(html)
    
    root = lxml.html.fromstring(html_page)
    r = root.cssselect('div.contactCard')
    # print r[0].text_content()
    for x in r:
        trs = x.cssselect("tr")
        tds = x.cssselect("td")
        for y in trs:
            if address_count < 8:
                data = { 'address': tds[1].text_content() }
                print "kerblaawww!!!"
                print tds[1].text_content()
                # print data
                keep_data = data['address']
                # arr_data = keep_data.split(' ')
                print keep_data
                # print arr_data
                final_data = {'name': '', 'address': '', 'address_2': '', 'city': '', 'state': 'CA', 'zip': 00000, 'phone': 555-555-5555, 'fax': 5}
                scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address_count, "bbb":keep_data})
                address_count+=1
            else:
                data = { 'address': tds[0].text_content() }
                keep_data = data['address']
                print data['address']
                scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address_count, "bbb":keep_data})
                address_count+=1

    page_count+=1
    
    
    print page_count   

print "END OF DOCUMENT"