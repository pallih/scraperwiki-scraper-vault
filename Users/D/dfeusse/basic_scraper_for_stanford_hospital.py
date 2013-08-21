import scraperwiki



import lxml
import lxml.html
import lxml.etree

imdbSite = lxml.html.parse("http://stanfordhospital.org/newsEvents/")
htmlNode = imdbSite.xpath("//h1")

lxml.etree.tostring(htmlNode[0])

print(htmlNode[0].text)



