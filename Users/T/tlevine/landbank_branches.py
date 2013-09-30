from scraperwiki.sqlite import save
from scraperwiki import swimport
keyify=swimport('keyify').keyify
from lxml.html import fromstring
from urllib2 import urlopen
URL='http://www.landbank.co.za/contact/branches.php'
from time import time
strip_address = swimport('strip_address').strip_address

DATE=time()

def main():
  blocks=get_blocks()
  blockId=0
  for block in blocks:
    blockId+=1
    block_info=block.data()
    block_info['blockId']=blockId
    block_info['date_scraped']=DATE
    save([],block_info,'blocks')
    for branch in block.branches():
      branch_info=branch.data()
      branch_info['blockId']=blockId
      branch_info['date_scraped']=DATE
      save([],branch_info,'branches')

def get_blocks():
  x=fromstring(urlopen(URL).read())
  blocks=x.xpath('//div[div[@class="float_info_left"]]')
  return [Block(block) for block in blocks]

class Block:
  def __init__(self,block):
    self.block=block

  def __str__(self):
    title,person=self.header()
    return title

  def header(self):
    title,person=self.block.xpath('preceding-sibling::strong[position()<=2]/text()')
    return title,person

  def region(self):
    return self.block.xpath('preceding-sibling::div[div[@class="darker"]]/div/h3/text()')[-1]

  def branch_names(self):
    return self.block.xpath('descendant::strong/text()')

  def data(self):
    title,person=self.header()
    return {
      "blockName":title
    , "blockPerson":person
    , "region":self.region()
    }

  def branches(self):
    b=[]
    for branch_name in self.branch_names():
      nodes=self.block.xpath('descendant::p[strong/text()="%s"]'%branch_name)
      assert len(nodes)==1
      b.append(Branch(nodes[0]))
    return b

class Branch:
  def __init__(self,p):
    self.p=p

  def __str__(self):
    return self.name()

  def name(self):
    nodes=self.p.xpath('strong/text()')
    assert 1==len(nodes)
    return nodes[0]

  def address(self):
    return '\n'.join(self.p.xpath('text()'))

  def phonecount(self):
    return len(self.b_text())

  def address_sans_phone(self):
    return '\n'.join(self.p.xpath('text()')[0:-self.phonecount()])

  def postcode(self):
    return self.p.xpath('text()')[-self.phonecount()-1]

  def town(self):
    return self.p.xpath('text()')[-self.phonecount()-2]

  def street_address(self):
    return '\n'.join(self.p.xpath('text()')[0:-self.phonecount()-2])

  def b_text(self):
    return self.p.xpath('b/text()')

  def phones(self):
    numbers=self.p.xpath('text()')[-self.phonecount():]
    return zip(self.b_text(),numbers)

  def data(self):
    d=dict([ (keyify(phone[0]),phone[1]) for phone in self.phones() ])
    d.update({
      "branchName":self.name()
    , "address_raw":self.address()
    , "town":strip_address(self.town())
    , "address":strip_address(self.address_sans_phone())
    , "street-address":strip_address(self.street_address())
    , "postcode":strip_address(self.postcode())
    })
    return d

main()from scraperwiki.sqlite import save
from scraperwiki import swimport
keyify=swimport('keyify').keyify
from lxml.html import fromstring
from urllib2 import urlopen
URL='http://www.landbank.co.za/contact/branches.php'
from time import time
strip_address = swimport('strip_address').strip_address

DATE=time()

def main():
  blocks=get_blocks()
  blockId=0
  for block in blocks:
    blockId+=1
    block_info=block.data()
    block_info['blockId']=blockId
    block_info['date_scraped']=DATE
    save([],block_info,'blocks')
    for branch in block.branches():
      branch_info=branch.data()
      branch_info['blockId']=blockId
      branch_info['date_scraped']=DATE
      save([],branch_info,'branches')

def get_blocks():
  x=fromstring(urlopen(URL).read())
  blocks=x.xpath('//div[div[@class="float_info_left"]]')
  return [Block(block) for block in blocks]

class Block:
  def __init__(self,block):
    self.block=block

  def __str__(self):
    title,person=self.header()
    return title

  def header(self):
    title,person=self.block.xpath('preceding-sibling::strong[position()<=2]/text()')
    return title,person

  def region(self):
    return self.block.xpath('preceding-sibling::div[div[@class="darker"]]/div/h3/text()')[-1]

  def branch_names(self):
    return self.block.xpath('descendant::strong/text()')

  def data(self):
    title,person=self.header()
    return {
      "blockName":title
    , "blockPerson":person
    , "region":self.region()
    }

  def branches(self):
    b=[]
    for branch_name in self.branch_names():
      nodes=self.block.xpath('descendant::p[strong/text()="%s"]'%branch_name)
      assert len(nodes)==1
      b.append(Branch(nodes[0]))
    return b

class Branch:
  def __init__(self,p):
    self.p=p

  def __str__(self):
    return self.name()

  def name(self):
    nodes=self.p.xpath('strong/text()')
    assert 1==len(nodes)
    return nodes[0]

  def address(self):
    return '\n'.join(self.p.xpath('text()'))

  def phonecount(self):
    return len(self.b_text())

  def address_sans_phone(self):
    return '\n'.join(self.p.xpath('text()')[0:-self.phonecount()])

  def postcode(self):
    return self.p.xpath('text()')[-self.phonecount()-1]

  def town(self):
    return self.p.xpath('text()')[-self.phonecount()-2]

  def street_address(self):
    return '\n'.join(self.p.xpath('text()')[0:-self.phonecount()-2])

  def b_text(self):
    return self.p.xpath('b/text()')

  def phones(self):
    numbers=self.p.xpath('text()')[-self.phonecount():]
    return zip(self.b_text(),numbers)

  def data(self):
    d=dict([ (keyify(phone[0]),phone[1]) for phone in self.phones() ])
    d.update({
      "branchName":self.name()
    , "address_raw":self.address()
    , "town":strip_address(self.town())
    , "address":strip_address(self.address_sans_phone())
    , "street-address":strip_address(self.street_address())
    , "postcode":strip_address(self.postcode())
    })
    return d

main()