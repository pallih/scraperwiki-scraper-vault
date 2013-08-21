from scraperwiki import swimport
from scraperwiki.sqlite import save
dsp=swimport('dsp').dsp
from time import time

DATE=time()

#Load
xml=dsp('http://www.tebabank.co.za/dist_atm.php',False)

#Parse
towns=xml.xpath('//ul[@class="bulletlist"]')

for town in towns:
  townnames=town.xpath('preceding-sibling::h2[position()=1]/text()')
  l=len(townnames)
  if l!=1:
    raise ParseError("There is supposed to be exactly one town name, but %d were found." % l)
  else:
    townname=townnames[0]

  addresses=town.xpath('li/text()')

  #Save
  for address in addresses:
    save([],{
      "town":townname
    , "address":address
    , "date_scraped":DATE
    },'swdata')
