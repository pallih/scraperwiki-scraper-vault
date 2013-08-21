import scraperwiki
import lxml.html 

# Blank Python

rooturl = "http://www.olympic.it/english/game/id_S"

for i in range(1,17):
    year = 1944 + 4*i
    html = scraperwiki.scrape(rooturl+str(year))
          
    root = lxml.html.etree.HTML(html)
    tdata = root.xpath("html::table[1]")
    print tdata    

    for tr in tdata:
        data = {
          'year' : year,
          'rank' : tr.text_content(),
          'country' : tr[1].text_content()
        }
        print data