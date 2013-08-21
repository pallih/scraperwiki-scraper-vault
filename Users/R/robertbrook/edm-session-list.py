import scraperwiki
import lxml.etree           

ES_NAMESPACE = "http://data.parliament.uk/services/edmi/session"
ES = "{%s}" % ES_NAMESPACE

tree = lxml.etree.parse("http://data.parliament.uk/EDMi/EDMi.svc/Session/List")
root = tree.getroot()
sessions = root.findall(".//%sSession" % ES)

for session in sessions:
      print session

# http://data.parliament.uk/EDMi/EDMi.svc/Session/List

