
import scraperwiki           
import lxml.html
import lxml.etree

import re
scraperwiki.sqlite.attach("isba_town_district","list")
print scraperwiki.sqlite.execute("select * from list.swdata")


root_url = "http://www.postar.co.uk/geography/town-and-district-codes?page="
initial_page = 1
final_page = 186

for n in range(initial_page,final_page+1):
    print n
    html = scraperwiki.scrape(root_url + str(n) )
    root = lxml.html.fromstring(html)
    the_list = root.xpath("//tbody/tr[td]") #

    for tr in the_list:
        tds = tr.cssselect("td")
        # District No.    District    Town No.    Town description
        data = {
            'district_no' : tds[0].text_content(),
            'district' : tds[2].text_content(),
            'town_no' : tds[3].text_content(),
            'town' : tds[4].text_content()
        }
        data['key'] = data['town_no']
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)
        print data


import scraperwiki           
import lxml.html
import lxml.etree

import re
scraperwiki.sqlite.attach("isba_town_district","list")
print scraperwiki.sqlite.execute("select * from list.swdata")


root_url = "http://www.postar.co.uk/geography/town-and-district-codes?page="
initial_page = 1
final_page = 186

for n in range(initial_page,final_page+1):
    print n
    html = scraperwiki.scrape(root_url + str(n) )
    root = lxml.html.fromstring(html)
    the_list = root.xpath("//tbody/tr[td]") #

    for tr in the_list:
        tds = tr.cssselect("td")
        # District No.    District    Town No.    Town description
        data = {
            'district_no' : tds[0].text_content(),
            'district' : tds[2].text_content(),
            'town_no' : tds[3].text_content(),
            'town' : tds[4].text_content()
        }
        data['key'] = data['town_no']
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)
        print data

