import scraperwiki

html = scraperwiki.scrape("http://www.elections.il.gov/CampaignDisclosure/A1List.aspx?ID=7465&FiledDocID=442719&ContributionType=AllTypes&Archived=True")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("ctl00_ContentPlaceHolder1_tblA1List"):
    tds = tr.cssselect('td')
    data = {
        'name' : tds[0].text_content(),
        'contribs' : int(tds[2].text_content()) 
    }
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)