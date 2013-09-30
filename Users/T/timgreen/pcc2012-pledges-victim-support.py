import scraperwiki
import lxml.html
import re
# Blank Python

url = "http://www.victimsupport.org.uk/About-us/Campaigns/Vote-for-victims/Candidates-whove-signed-up"

tree = lxml.html.parse(url)

pattern = re.compile('(.*?) \((.*?), (.*?)\)')

for p in tree.xpath("//div[@id='mainContent']//li"):

  data = pattern.match(p.text_content().strip())

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

url = "http://www.victimsupport.org.uk/About-us/Campaigns/Vote-for-victims/Candidates-whove-signed-up"

tree = lxml.html.parse(url)

pattern = re.compile('(.*?) \((.*?), (.*?)\)')

for p in tree.xpath("//div[@id='mainContent']//li"):

  data = pattern.match(p.text_content().strip())

  if data is None:
    pass
  else:
    name, party, place = data.groups()

    pledge = {'name': name,
              'party': party,
              'place': place,}

    scraperwiki.sqlite.save(['name', 'place'], pledge, table_name='pledges')
