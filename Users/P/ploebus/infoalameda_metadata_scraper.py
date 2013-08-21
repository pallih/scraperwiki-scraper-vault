# Blank Python
import scraperwiki           
html = scraperwiki.scrape("http://www.infoalamedacounty.org/index.php/Data/Metadata-Sources.html")
BASEURL='http://www.infoalamedacounty.org'

import lxml.html           
root = lxml.html.fromstring(html)
titles=root.cssselect("h3.catItemTitle")
index=1
for title in titles:
    links=title.iterlinks()
    for link in links:
        html1=scraperwiki.scrape(BASEURL+link[2])
        root1 = lxml.html.fromstring(html1)
        rows1=root1.cssselect("table tr")
        for row1 in rows1:
            record={}
            table_cells=row1.cssselect("td")
            if table_cells:
                record['id']=index
                record['Source']=title.text_content().strip()
                record['Key']=table_cells[0].text_content()
                record['Value']=table_cells[1].text_content()
                index=index+1
                print index
                print record
                scraperwiki.sqlite.save(unique_keys=['id','Source','Value'],data=record)
                

               
    
#rows=root.cssselect("table tr")
#for row in rows:
#    record={}
#    table_cells=row.cssselect("td")
#    if table_cells:
#        record['Source']="Alameda County Public Health Department"
#        record['Key']=table_cells[0].text_content()
#        record['Value']=table_cells[1].text_content()
#        print record
#        scraperwiki.datastore.save(["Key"],record)