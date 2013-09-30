import scraperwiki

#for Nordic Development Fund
html = scraperwiki.scrape("http://www.ndf.fi/index.php?id=68") #Africa

import lxml.html
root = lxml.html.fromstring(html)

tds = root.cssselect("div[class='mcmain'] strong") # get all the <td> tags
for td in tds:
    print lxml.html.tostring(td) # the full HTML tag
    print td.text                # just the text inside the HTML tag
for td in tds:
     if td.text:
         record = { "p" : td.text } # column name and value
         scraperwiki.sqlite.save(["p"], record) # save the records one by one


#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==6:
#        data = {
#            'country_project' : tds[0].text_content(),
#            'sector' : tds[1].text_content(),
#            'lead_agency' : tds[2].text_content(),
#            'investment_million_ndf' : tds[3].text_content(),
#            'total' : tds[4].text_content(),
#            'year_of_signing' : tds[5].text_content(),
#        }
#        scraperwiki.sqlite.save(unique_keys=['country_project'], data=data)



import scraperwiki

#for Nordic Development Fund
html = scraperwiki.scrape("http://www.ndf.fi/index.php?id=68") #Africa

import lxml.html
root = lxml.html.fromstring(html)

tds = root.cssselect("div[class='mcmain'] strong") # get all the <td> tags
for td in tds:
    print lxml.html.tostring(td) # the full HTML tag
    print td.text                # just the text inside the HTML tag
for td in tds:
     if td.text:
         record = { "p" : td.text } # column name and value
         scraperwiki.sqlite.save(["p"], record) # save the records one by one


#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==6:
#        data = {
#            'country_project' : tds[0].text_content(),
#            'sector' : tds[1].text_content(),
#            'lead_agency' : tds[2].text_content(),
#            'investment_million_ndf' : tds[3].text_content(),
#            'total' : tds[4].text_content(),
#            'year_of_signing' : tds[5].text_content(),
#        }
#        scraperwiki.sqlite.save(unique_keys=['country_project'], data=data)



