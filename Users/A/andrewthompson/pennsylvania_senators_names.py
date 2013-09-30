import scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.legis.state.pa.us/cfdocs/legis/home/member_information/mbrList.cfm?body=S&sort=alpha")

import lxml.html           
root = lxml.html.fromstring(html)
for div in root.cssselect("div[class='container'] div[class='mbr']"):
    
    text = div.text_content()
    districttext = text[text.index("District"):-7]
    districtnumber = districttext[9:]
    #print districttext
    #print districtnumber

    bs = div.cssselect("b")
    ahrefs = bs[0].cssselect("a")
    whole_name = ahrefs[0].text_content()
    last_name = whole_name[:whole_name.index(",")].strip()
    
    data = { 'last_name' : last_name.strip(), 'district_number' : districtnumber.strip(), 'whole_name' : whole_name.strip(), 'district' : districttext.strip() }

    scraperwiki.sqlite.save(unique_keys=['last_name'], data=data)
    
import scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.legis.state.pa.us/cfdocs/legis/home/member_information/mbrList.cfm?body=S&sort=alpha")

import lxml.html           
root = lxml.html.fromstring(html)
for div in root.cssselect("div[class='container'] div[class='mbr']"):
    
    text = div.text_content()
    districttext = text[text.index("District"):-7]
    districtnumber = districttext[9:]
    #print districttext
    #print districtnumber

    bs = div.cssselect("b")
    ahrefs = bs[0].cssselect("a")
    whole_name = ahrefs[0].text_content()
    last_name = whole_name[:whole_name.index(",")].strip()
    
    data = { 'last_name' : last_name.strip(), 'district_number' : districtnumber.strip(), 'whole_name' : whole_name.strip(), 'district' : districttext.strip() }

    scraperwiki.sqlite.save(unique_keys=['last_name'], data=data)
    
