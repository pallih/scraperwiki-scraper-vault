from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
from time import time, sleep

DATE = time()
DIR = 'http://www.bpr.rw/'
MENU = "http://www.bpr.rw/spip.php?rubrique2"

def main():
  hrefs = parsebranches()
  for href in hrefs:
    sleep(3)
    branchinfo(href)

def branchinfo(href):
  x=fromstring(urlopen(DIR + href).read())
  for thingtype in ("Sub-Branches", "Outlets"):
    locations = [loc.strip() for loc in x.xpath('//p[strong/text()="%s"]/following-sibling::p[position()=1]/text()' % thingtype)]
    d = [{"location": location, "date_scraped": DATE, "branch-href": href} for location in locations]
    save([], d, "branch_" + thingtype)

def parsebranches():
  x=fromstring(urlopen(MENU).read())
  branches = x.xpath('//td[@style="padding:4px;background-image:url(squelettes/bpr_imgs/bpr_innermaintitlesbg.gif);background-repeat:no-repeat;background-position:right bottom;"]')
  d = []
  for branch in branches:
    row = parsebranch(branch)
    row['date_scraped'] = DATE
    d.append(row)
  save([], d, 'branches')
  return [b['href'] for b in d]

def parsebranch(branch):
  textnodes = branch.xpath('font/text()')
  branchlinks = branch.xpath('a[position()=1 and @class="bpr_networklink"]')
  assert len(branchlinks) == 1
  branchlink = branchlinks[0]

  cleannodes = [n[1:] for n in textnodes[1:]]
  branchdata = dict([cleannode.split(':') for cleannode in cleannodes])

  assert set(branchdata.keys()).issubset(['BP', 'Fax', 'Tel']), branchdata

  branchdata.update({
    "region":textnodes[0]
  , "name":branchlink.text
  , "href":branchlink.attrib['href']
  })

  return branchdata

main()
#branchinfo("spip.php?rubrique11")from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
from time import time, sleep

DATE = time()
DIR = 'http://www.bpr.rw/'
MENU = "http://www.bpr.rw/spip.php?rubrique2"

def main():
  hrefs = parsebranches()
  for href in hrefs:
    sleep(3)
    branchinfo(href)

def branchinfo(href):
  x=fromstring(urlopen(DIR + href).read())
  for thingtype in ("Sub-Branches", "Outlets"):
    locations = [loc.strip() for loc in x.xpath('//p[strong/text()="%s"]/following-sibling::p[position()=1]/text()' % thingtype)]
    d = [{"location": location, "date_scraped": DATE, "branch-href": href} for location in locations]
    save([], d, "branch_" + thingtype)

def parsebranches():
  x=fromstring(urlopen(MENU).read())
  branches = x.xpath('//td[@style="padding:4px;background-image:url(squelettes/bpr_imgs/bpr_innermaintitlesbg.gif);background-repeat:no-repeat;background-position:right bottom;"]')
  d = []
  for branch in branches:
    row = parsebranch(branch)
    row['date_scraped'] = DATE
    d.append(row)
  save([], d, 'branches')
  return [b['href'] for b in d]

def parsebranch(branch):
  textnodes = branch.xpath('font/text()')
  branchlinks = branch.xpath('a[position()=1 and @class="bpr_networklink"]')
  assert len(branchlinks) == 1
  branchlink = branchlinks[0]

  cleannodes = [n[1:] for n in textnodes[1:]]
  branchdata = dict([cleannode.split(':') for cleannode in cleannodes])

  assert set(branchdata.keys()).issubset(['BP', 'Fax', 'Tel']), branchdata

  branchdata.update({
    "region":textnodes[0]
  , "name":branchlink.text
  , "href":branchlink.attrib['href']
  })

  return branchdata

main()
#branchinfo("spip.php?rubrique11")