import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=ST4++7HG&Coords=3454%2c3871&ServiceType=WalkInCentre&JScript=1&PageCount=13&PageNumber=1")
root = lxml.html.fromstring(html)
for el in root.cssselect("ul.results li"):
    print el
import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=ST4++7HG&Coords=3454%2c3871&ServiceType=WalkInCentre&JScript=1&PageCount=13&PageNumber=1")
root = lxml.html.fromstring(html)
for el in root.cssselect("ul.results li"):
    print el
