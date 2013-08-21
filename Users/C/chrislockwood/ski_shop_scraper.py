import scraperwiki
# Baseball Field Scraper
import lxml.html


# Webpage to be scraped
html = scraperwiki.scrape ("https://www.seattle.gov/parks/baseball.asp")
#print html

root = lxml.html.fromstring (html)
#print len(root.cssselect("table"))

#print lxml.html.tostring(root.cssselect("table")[5])

#print len(root.cssselect("table")[5].cssselect("table tr"))
# due to the multiple tables within the source this selects the 5th table in the set. 
for tr in root.cssselect("table")[5].cssselect("tr")[1:]:
    
    #print lxml.html.tostring(tr)
# Set working_table to select everything within the "tr"
    working_table = root.cssselect("table")[5].cssselect("tr")[1:]
# ran a for loup to print out the "td" content within "tr"
for tr in working_table:
    
# ran an if statement to select only data from td.trow and not td.trowB
    if len(tr.cssselect("td.trow"))==2:
        
        print tr.cssselect("td")[0].text_content()
            
        print tr.cssselect("td")[1].text_content().split("(")[0]

        tds = tr.cssselect("td")   
    
        data = {
            'FieldName': tr.cssselect("td")[0].text_content(),
            'Address': tr.cssselect("td")[1].text_content().split("(")[0]
        }    
        scraperwiki.sqlite.save(unique_keys=['FieldName'],data=data)
        
    


    
