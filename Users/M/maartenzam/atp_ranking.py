import scraperwiki
import lxml.html 

rooturl = "http://www.atpworldtour.com/Rankings/Singles.aspx?d=01.01."

for year in range(2000, 2013):
    for rank in range(0, 16):
        r=rank*100+1
        html = scraperwiki.scrape(rooturl+str(year)+'&r='+str(r))
          
        root = lxml.html.fromstring(html)
    
        for tr in root.cssselect("table.bioTableAlt tr"):
            tds = tr.cssselect("td")
            key = str(year)+","+tds[0].text_content().replace("u'", "").replace("\t", "").replace("\n", "").replace("\r", " ")
            data = {
              'key' : key,
              'year' : year,
              'text' : tds[0].text_content().replace("u'", "").replace("\t", "").replace("\n", "").replace("\r", " "),
              'points': tds[1].text_content().replace(",", "")
            }
            scraperwiki.sqlite.save(unique_keys=['key'], data=data)