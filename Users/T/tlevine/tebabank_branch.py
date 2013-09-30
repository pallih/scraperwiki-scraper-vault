from scraperwiki import swimport
from scraperwiki.sqlite import save
from time import time
DATE=time()
strip_address = swimport('strip_address').strip_address

#Load
xml=swimport('dsp').dsp('http://www.tebabank.co.za/dist_branch_locs.php',False)

#Parse
towns=xml.xpath('//div[@class="adresswrap"]/h2/text()')
address_nodes=xml.cssselect('div.adresswrap > p')
messes=['\n'.join(address_node.xpath('text()')) for address_node in address_nodes]

d=[dict(zip(["address","phone"],mess.split('Tel:'))) for mess in messes]
for row,town in zip(d,towns):
  row["town"]=town
  row["date_scraped"]=DATE
  row["address"] = strip_address(row["address"])

#Save
save([],d)
from scraperwiki import swimport
from scraperwiki.sqlite import save
from time import time
DATE=time()
strip_address = swimport('strip_address').strip_address

#Load
xml=swimport('dsp').dsp('http://www.tebabank.co.za/dist_branch_locs.php',False)

#Parse
towns=xml.xpath('//div[@class="adresswrap"]/h2/text()')
address_nodes=xml.cssselect('div.adresswrap > p')
messes=['\n'.join(address_node.xpath('text()')) for address_node in address_nodes]

d=[dict(zip(["address","phone"],mess.split('Tel:'))) for mess in messes]
for row,town in zip(d,towns):
  row["town"]=town
  row["date_scraped"]=DATE
  row["address"] = strip_address(row["address"])

#Save
save([],d)
