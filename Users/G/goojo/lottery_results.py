import scraperwiki
import lxml.html           
import re

html = scraperwiki.scrape("http://www.bbc.co.uk/lottery/")
root = lxml.html.fromstring(html)

for x in root.cssselect("div.draws-lotto"):
    drawnumber = x.cssselect("span.draw")
    results = x.cssselect("ul.draws")
    date = x.cssselect("p")

    index = 0
    for y in drawnumber: 
        balls = results[index].cssselect("li.balls")
        data = {
                'draw' : re.sub("\D","",y.text_content()),
                'b1' : balls[0].text_content(),
                'b2' : balls[1].text_content(),                
                'b3' : balls[2].text_content(),                
                'b4' : balls[3].text_content(),
                'b5' : balls[4].text_content(),
                'b6' : balls[5].text_content(),
                'bb' : balls[6].text_content(),
                'date' : date[index].text_content().strip()
                }        
        index=index+1
        scraperwiki.sqlite.save(unique_keys=['draw'], data=data)
        print (data)
