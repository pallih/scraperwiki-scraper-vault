import scraperwiki
import lxml.html           
html = scraperwiki.scrape('http://www.onthesnow.com/open_resorts_all.html?startRow=0&numRows=500')
root = lxml.html.fromstring(html)
rows = root.cssselect('tr')
link=root.cssselect('a')
for row in rows: 
    record={}
    table_cells = row.cssselect("td")
    if len(row)>=6:
        record['ResortName'] =  table_cells[0].text_content()
        record['LiftsOpen'] =  table_cells[1].text
        record['DaySnowfall'] =  table_cells[2].text
        record['BaseDepth'] =  table_cells[3].text    
        #print record, '------------' 
        scraperwiki.sqlite.save(["ResortName"], record)