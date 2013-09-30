import lxml.html          
import scraperwiki 
import dateutil.parser 

# download one page 

html = scraperwiki.scrape( "http://spring96.org/persecution/?DateFrom=2000-01-01&DateTo=2012-12-31&Page=0&PrintAll=1" )
root = lxml.html.fromstring(html)

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)==10:
        data = {
            'Number' : int(tds[0].text_content()),
            'Date' : tds[1].text_content().strip(),
            'Name' : tds[2].text_content().strip(),
            'Article of law' : tds[3].text_content().strip(),
            'Date of trial' : tds[4].text_content().strip(),
            'Judge' : tds[5].text_content().strip(),
            'Court' : tds[6].text_content().strip(),
            'Arrest' : tds[7].text_content().strip(),
            'Fine' : tds[8].text_content().strip(),
            'Remarks' : tds[9].text_content().strip(),
        }
        scraperwiki.sqlite.save(unique_keys=['Number'], data=data)





import lxml.html          
import scraperwiki 
import dateutil.parser 

# download one page 

html = scraperwiki.scrape( "http://spring96.org/persecution/?DateFrom=2000-01-01&DateTo=2012-12-31&Page=0&PrintAll=1" )
root = lxml.html.fromstring(html)

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)==10:
        data = {
            'Number' : int(tds[0].text_content()),
            'Date' : tds[1].text_content().strip(),
            'Name' : tds[2].text_content().strip(),
            'Article of law' : tds[3].text_content().strip(),
            'Date of trial' : tds[4].text_content().strip(),
            'Judge' : tds[5].text_content().strip(),
            'Court' : tds[6].text_content().strip(),
            'Arrest' : tds[7].text_content().strip(),
            'Fine' : tds[8].text_content().strip(),
            'Remarks' : tds[9].text_content().strip(),
        }
        scraperwiki.sqlite.save(unique_keys=['Number'], data=data)





