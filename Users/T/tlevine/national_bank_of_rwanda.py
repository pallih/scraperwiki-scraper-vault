from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
from time import time, sleep
import re
#from unidecode import unidecode
def unidecode(foo):
  return foo

DATE = time()
URL = "http://www.bnr.rw/supervision/bankregister.aspx"


def main():
  x = fromstring(urlopen(URL).read())
  bank_trs = x.xpath('//tr[td[@class="titlecell"]]')
  d = []
  for tr in bank_trs:
    b = Bank(tr)
    row = b.tablerow()
    row['date_scraped'] = DATE
    d.append(row)
  save([], d, 'institutions')

class Bank:
  class UnknownClass(Exception):
    pass

  def __init__(self,tr):
    self.tr = tr

  def name(self):
    return self.trtext(self.tr)

  @staticmethod
  def trtext(tr):
    nodes = tr.xpath('td/text()')
    assert 1 == len(nodes)
    return nodes[0]

  def tablerow(self):
    infolist = self.infolist()
    infodict = {"name": self.name()}

    if len(infolist) > 0 and "http" in infolist[-1]:
      infodict['website'] = re.sub(r'^.*: ', '', infolist.pop())

    if len(infolist) > 0 and "Telephone" in infolist[-1]:
      infodict['phone'] = infolist.pop()

    if len(infolist) > 0 and "Licensed" not in infolist[-1]:
      infodict['address'] = infolist.pop()

    if len(infolist) > 0 and "Licensed" in infolist[-1]:
      infodict['licensed'] = int(re.findall(r'[0-9]{4}', infolist.pop())[0])

    return infodict

  def infolist(self):
    "Pick out the following trs that pertain to the current bank."
    trs = self.tr.xpath('following-sibling::tr')

    info = []
    for tr in trs:
      a = tr.xpath('td')[0].attrib
      if a.has_key('class') and a['class'] == 'description':
        #info.append(self.trtext(tr))
        info.append(unidecode(tr.text_content().strip()))
      elif a.has_key('class') and a['class'] == 'titlecell':
        break
      else:
        UnknownClass('''This tr's class attribute neither "titlecell" nor "description".''')
    return info

main()from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen
from time import time, sleep
import re
#from unidecode import unidecode
def unidecode(foo):
  return foo

DATE = time()
URL = "http://www.bnr.rw/supervision/bankregister.aspx"


def main():
  x = fromstring(urlopen(URL).read())
  bank_trs = x.xpath('//tr[td[@class="titlecell"]]')
  d = []
  for tr in bank_trs:
    b = Bank(tr)
    row = b.tablerow()
    row['date_scraped'] = DATE
    d.append(row)
  save([], d, 'institutions')

class Bank:
  class UnknownClass(Exception):
    pass

  def __init__(self,tr):
    self.tr = tr

  def name(self):
    return self.trtext(self.tr)

  @staticmethod
  def trtext(tr):
    nodes = tr.xpath('td/text()')
    assert 1 == len(nodes)
    return nodes[0]

  def tablerow(self):
    infolist = self.infolist()
    infodict = {"name": self.name()}

    if len(infolist) > 0 and "http" in infolist[-1]:
      infodict['website'] = re.sub(r'^.*: ', '', infolist.pop())

    if len(infolist) > 0 and "Telephone" in infolist[-1]:
      infodict['phone'] = infolist.pop()

    if len(infolist) > 0 and "Licensed" not in infolist[-1]:
      infodict['address'] = infolist.pop()

    if len(infolist) > 0 and "Licensed" in infolist[-1]:
      infodict['licensed'] = int(re.findall(r'[0-9]{4}', infolist.pop())[0])

    return infodict

  def infolist(self):
    "Pick out the following trs that pertain to the current bank."
    trs = self.tr.xpath('following-sibling::tr')

    info = []
    for tr in trs:
      a = tr.xpath('td')[0].attrib
      if a.has_key('class') and a['class'] == 'description':
        #info.append(self.trtext(tr))
        info.append(unidecode(tr.text_content().strip()))
      elif a.has_key('class') and a['class'] == 'titlecell':
        break
      else:
        UnknownClass('''This tr's class attribute neither "titlecell" nor "description".''')
    return info

main()