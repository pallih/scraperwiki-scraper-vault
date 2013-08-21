import scraperwiki
from lxml import etree

countryIncomeLevels = etree.parse("http://api.worldbank.org/incomeLevels/LIC/countries?format=xml")
print etree.tostring(countryIncomeLevels.getroot())

for el in countryIncomeLevels.iter():
    print("%s - %s" % (el.tag, el.text))
