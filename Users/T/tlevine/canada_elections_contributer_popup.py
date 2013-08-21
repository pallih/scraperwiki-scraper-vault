from scraperwiki.sqlite import save,attach,select
from lxml.html import fromstring
from urllib2 import urlopen

BASEURL="http://www.elections.ca/scripts/webpep/fin2/contributor.aspx?"
TEST_QUERYSTRING="type=1&client=21612&row=3995665&seqno=&part=2a&entity=1&lang=e&option=4&return=1"

def main():
  attach('canada_elections_contributer_table')
  for qs in select('querystring from contributions where querystring not in (select querystring from contributors)'):
    popup(qs)

def _subspan_text(element):
  return element.getchildren()[0].text

def _keyify(key):
  return key.encode('ascii','ignore').replace(':','')

def popup(d):
  xml=fromstring(urlopen(BASEURL+d['querystring']).read())
  for tr in xml.xpath('//tr[td[@width="36%"]]'):
    tds=tr.getchildren()
    while(len(tds)>0):
      key=tds.pop(0)
      value=tds.pop(0)
      d[_keyify(_subspan_text(key))]=_subspan_text(value)
  save(["querystring"],d,'contributors')

#popup(TEST_QUERYSTRING)
main()