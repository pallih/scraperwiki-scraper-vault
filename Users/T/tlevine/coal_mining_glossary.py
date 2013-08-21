"""

This is a glossary of mining terms from the "Kentucky Coal and Energy Education Project":http://www.coaleducation.org/glossary.htm.

h3. Cool mining terms

These might make fun names for something.

* blasting cap
* carbide bit
* anemometer
* highwall
* mudcap
* torque wrench

"""
from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring,tostring

def main():
  x=fromstring(urlopen('http://www.coaleducation.org/glossary.htm').read())
  entries=x.xpath('//p[span[@class="style13"]]')
  d=parse_glossary(entries)
  print len(d)
  save(['term'],d,'glossary')

def parse_glossary(entries):
  d=[]
  for entry in entries:
    d.append({
      "definition":getone(entry,'span[@class="style13"]').text_content()[2:]
    , "term":getone(entry,'*[self::span[@class="style14"] or self::a]').text_content()
    })
  return d

def getone(tree,path):
  nodes=tree.xpath(path)
  assert 1==len(nodes),map(tostring,nodes)
  return nodes[0]

main()