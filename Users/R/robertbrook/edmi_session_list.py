import scraperwiki
from lxml import etree

xml = scraperwiki.scrape("http://data.parliament.uk/EDMi/EDMi.svc/Session/List")

session_results = etree.XML(xml)

sessions_list = session_results.find("{http://data.parliament.uk/services/edmi/session}Sessions")

sessions = sessions_list.findall("{http://data.parliament.uk/services/edmi/session}Session")

for session in sessions:
    data = {
      'id' : session.attrib["id"],
      'value' : session.find("{http://data.parliament.uk/services/edmi/session}SessionValue").text,
      'startdate' : session.find("{http://data.parliament.uk/services/edmi/session}SessionStartDate").text,
      'enddate' : session.find("{http://data.parliament.uk/services/edmi/session}SessionEndDate").text
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)