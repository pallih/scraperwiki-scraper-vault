import scraperwiki
import lxml.html

print("Scraping Mozambique microfinance data")

# Pull in html data
html = scraperwiki.scrape("http://www.bancomoc.mz/Instituicoes_en.aspx?id=GINS0017&ling=en")
#print(html)

root = lxml.html.fromstring(html) 
names = lxml.html.find_class(root, 'main-table')
print(names)

#for tr in names.cssselect("div[align='left'] tr.tcont"): 
#    tds = tr.cssselect("td") 
#    data = { 
#      'rawdata' : tds[0].text_content(), 
#    } 
#    print data


import scraperwiki
import lxml.html

print("Scraping Mozambique microfinance data")

# Pull in html data
html = scraperwiki.scrape("http://www.bancomoc.mz/Instituicoes_en.aspx?id=GINS0017&ling=en")
#print(html)

root = lxml.html.fromstring(html) 
names = lxml.html.find_class(root, 'main-table')
print(names)

#for tr in names.cssselect("div[align='left'] tr.tcont"): 
#    tds = tr.cssselect("td") 
#    data = { 
#      'rawdata' : tds[0].text_content(), 
#    } 
#    print data


