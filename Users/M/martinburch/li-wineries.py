import scraperwiki
import lxml.html

# A list of Long Island wineries from the Long Island Wine Council
html = scraperwiki.scrape("http://www.liwines.com/?cat=7")
root = lxml.html.fromstring(html)

searchstring = ""

for el in root.xpath('//*[@id="individualboxtextarea"]/a[1]'):
    searchstring += '"' + el.text + '",'

print searchstring
