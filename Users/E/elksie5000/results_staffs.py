import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.thisisstaffordshire.co.uk/search/search.html?searchPhrase=stoke&where=&searchType=&orderByOption=dateDesc")
root = lxml.html.fromstring(html)


for el in root.cssselect("ul.results-list  h2"):
    print el.text_content():

    #print lxml.html.tostring(el)

    #print el

