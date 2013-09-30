import sys, scraperwiki, re
from lxml import etree
xml = scraperwiki.scrape("http://www.writetothem.com/stats/2008/mps?xml=1")
doc = etree.fromstring(xml)
for person in doc.findall("personinfo"):
    if (person.get("writetothem_responsiveness_mean_2008")):
        thisscore = re.sub('%', '', person.get("writetothem_responsiveness_mean_2008"))
    else:
        thisscore = ''
    data = {
      'id' : person.get("id"),
      'name' : person.get("name"),
      'constituency' : person.get("constituency"),
      'party' : person.get("party"),
      'score' : thisscore
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

import sys, scraperwiki, re
from lxml import etree
xml = scraperwiki.scrape("http://www.writetothem.com/stats/2008/mps?xml=1")
doc = etree.fromstring(xml)
for person in doc.findall("personinfo"):
    if (person.get("writetothem_responsiveness_mean_2008")):
        thisscore = re.sub('%', '', person.get("writetothem_responsiveness_mean_2008"))
    else:
        thisscore = ''
    data = {
      'id' : person.get("id"),
      'name' : person.get("name"),
      'constituency' : person.get("constituency"),
      'party' : person.get("party"),
      'score' : thisscore
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

