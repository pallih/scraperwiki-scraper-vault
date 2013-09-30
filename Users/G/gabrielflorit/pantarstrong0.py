import scraperwiki
html = scraperwiki.scrape("http://www.inc.com/inc5000/2009/search_results.html?showrank=on&b_rank=1&e_rank=5000&showstate=on&state=all&showname=on&name=Company+Name&showgrowth=on&b_growth=20&e_growth=316000&showregion=on&region=all&showindustry=on&industry=all&showrevenue=on&b_revenue=1000000&e_revenue=6000000000&showyear=on&b_year=1982&e_year=2009&showemployees=on&b_employees=1&e_employees=30200&showfounded=on&b_founded=1790&e_founded=2004&submit=Filter+the+List")

import lxml.html
root = lxml.html.fromstring(html)
listTable = root.get_element_by_id("listTable")
listTableTR = listTable.cssselect("tr")

counter = 0
columnNames = []
data = {}

for tr in listTableTR:
    
    if (counter == 0):
        for td in tr:
            textContent = td.text_content()
            columnNames.append(textContent)
            print textContent

    if (counter > 0):
        for td in tr:
            textContent = td.text_content()
            


    counter = counter + 1

print len(columnNames)





#root = lxml.html.fromstring(html)
#for tr in root.cssselect("table[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    print data

import scraperwiki
html = scraperwiki.scrape("http://www.inc.com/inc5000/2009/search_results.html?showrank=on&b_rank=1&e_rank=5000&showstate=on&state=all&showname=on&name=Company+Name&showgrowth=on&b_growth=20&e_growth=316000&showregion=on&region=all&showindustry=on&industry=all&showrevenue=on&b_revenue=1000000&e_revenue=6000000000&showyear=on&b_year=1982&e_year=2009&showemployees=on&b_employees=1&e_employees=30200&showfounded=on&b_founded=1790&e_founded=2004&submit=Filter+the+List")

import lxml.html
root = lxml.html.fromstring(html)
listTable = root.get_element_by_id("listTable")
listTableTR = listTable.cssselect("tr")

counter = 0
columnNames = []
data = {}

for tr in listTableTR:
    
    if (counter == 0):
        for td in tr:
            textContent = td.text_content()
            columnNames.append(textContent)
            print textContent

    if (counter > 0):
        for td in tr:
            textContent = td.text_content()
            


    counter = counter + 1

print len(columnNames)





#root = lxml.html.fromstring(html)
#for tr in root.cssselect("table[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    print data

