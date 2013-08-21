import scraperwiki
import lxml.html, lxml.cssselect
import re

rssurl="http://www.sec.gov/Archives/edgar/usgaap.rss.xml"

# load
root = lxml.html.parse(rssurl).getroot()


#parse
for item in root.cssselect('rss > channel > item'):
  d1 = (item.cssselect('companyname')[0]).text
  d2  = (item.cssselect('ciknumber')[0]).text
  d3  = (item.cssselect('filingdate')[0]).text
  # new record
  record = {}
  record['company name'] = d1
  record['cik'] = d2
  record['filingdate'] = d3
  # parse more
  for filing in item.cssselect('xbrlfile'):
    descr = filing.attrib.get('edgar:description')
    d5 = filing.attrib.get('edgar:url')
    record['uri'] = d5
    d4="UNKNOWN"
    if (re.match('.*INSTANCE DOCUMENT.*',descr)):
      d4 = "xbrl"
      record['type'] = d4
      #print d1+", "+d2+", "+d3+", "+d4+", "+d5
    else:
      type = filing.attrib.get('edgar:type')
      if (re.match('.*(10-Q).*',type)):
        d4 = type
        record['type'] = d4
        #print d1+", "+d2+", "+d3+", "+d4+", "+d5
    if (d1.find('UNKNOWN')==-1)
      record['id'] = d2+"_"+d3+"_"+d4
      #print record
      scraperwiki.sqlite.save(unique_keys=['id'], data=record)
