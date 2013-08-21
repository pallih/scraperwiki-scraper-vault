import scraperwiki
import lxml.html
import re
# Blank Python

url = "http://www.urboss.org.uk/campaigns/police-and-crime-commissioners-campaign"

tree = lxml.html.parse(url)

pattern = re.compile('(.*?) \((.*?), (.*?)\)')

for p in tree.xpath("//div[@id='myCarousel']//div/a/img/@alt"):
  print p

  if True:
    pledge = {'name': p,
              }

    scraperwiki.sqlite.save(['name'], pledge, table_name='pledges')
