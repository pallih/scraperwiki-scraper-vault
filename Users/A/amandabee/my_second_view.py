# Blank Python
import scraperwiki 

sourcescraper = 'my_second_scraper'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( 
    '''* from my_second_scraper.swdata order by price desc limit 100''' 
) 

for d in data: 
    print "<a href=",d["URL"],">", d["title"], "</a><br />" 
    print "Price:", d["price"], "<br />" 
    print d["nabe"], "/",d["category"],"<br />" 
    print "<img src=", d["image"], ">" 
    print "<hr />"

# Blank Python
import scraperwiki 

sourcescraper = 'my_second_scraper'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( 
    '''* from my_second_scraper.swdata order by price desc limit 100''' 
) 

for d in data: 
    print "<a href=",d["URL"],">", d["title"], "</a><br />" 
    print "Price:", d["price"], "<br />" 
    print d["nabe"], "/",d["category"],"<br />" 
    print "<img src=", d["image"], ">" 
    print "<hr />"

