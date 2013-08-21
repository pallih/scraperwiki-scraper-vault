import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.dice.com/job/rss/ga?b=1&caller=2&q=%22business+intelligence%22+%28senior+OR+sr+lead%29&src=18&t=2&x=boolean&p=s')
print rss

root = lxml.html.fromstring(rss) # turn our HTML into an lxml object
print root

for el in root.cssselect("div.featured a"):
    print el

#tds = root.cssselect('td') # get all the <td> tags
#for td in tds:
#    print lxml.html.tostring(td) # the full HTML tag
#    print td.text                # just the text inside the HTML ta

