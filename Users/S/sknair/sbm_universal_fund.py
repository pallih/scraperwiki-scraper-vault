import scraperwiki
html = scraperwiki.scrape('http://www.sbmmam.com/local_funds.php')

import lxml.html
tree = lxml.html.fromstring(html) # turn our HTML into an lxml object
trs= tree.xpath("//html/body/table[@id='Table_01']/tr[2]/td/table/tr/td[2]/table/tr[2]/td[2]/table/tr")

#print "<sbm_funds>"
for tr in (4, 5, 6, 7):
    tds = trs[tr] 
    
    record = {}
    
    record['Fund Name'] = tds[0].text
    record['Valuation Date'] = tds[2].text
    record['Issue Price'] = tds[3].text
    record['Repurchase Price'] = tds[5].text

    scraperwiki.sqlite.save(['Valuation Date']+['Fund Name'], record)
    #print "<product>"
    #tds = trs[tr] 
    #print "<name>%s</name>" % (tds[0].text)
    #print "<valuation_date>%s</valuation_date>" % (tds[2].text)
    #print "<issue_price>%s</issue_price>" % (tds[3].text)
    #print "<repurchase_price>%s</repurchase_price>" % (tds[5].text)
    #print "</product>"
#print "</sbm_funds>"

