import scraperwiki
import lxml.html
import re
# Blank Python

url = "http://www.barnardos.org.uk/get_involved/campaign/cutthemfree/candidatessupportingthecampaign.htm"

tree = lxml.html.parse(url)

pattern = re.compile('(.*?) \((.*?), (.*?)\)')

for p in tree.xpath("//div[@id='contentWide']/p"):
  data = pattern.match(p.text_content())
  if data is None:
    pass
  else:
    name, party, place = data.groups()

    pledge = {'name': name,
              'party': party,
              'place': place,}

    scraperwiki.sqlite.save(['name', 'place'], pledge, table_name='pledges')
import scraperwiki
import lxml.html
import re
# Blank Python

url = "http://www.barnardos.org.uk/get_involved/campaign/cutthemfree/candidatessupportingthecampaign.htm"

tree = lxml.html.parse(url)

pattern = re.compile('(.*?) \((.*?), (.*?)\)')

for p in tree.xpath("//div[@id='contentWide']/p"):
  data = pattern.match(p.text_content())
  if data is None:
    pass
  else:
    name, party, place = data.groups()

    pledge = {'name': name,
              'party': party,
              'place': place,}

    scraperwiki.sqlite.save(['name', 'place'], pledge, table_name='pledges')
