from scraperwiki.sqlite import save
from scraperwiki import swimport
import re
URL="http://www.landbank.co.za/contact/satellite_branches.php"
from time import time
DATE=time()

whitespace_start=re.compile(r'^[\t\n\r ]*')
whitespace_end=re.compile(r'[\t\n\r ]*$')

def main():
  x=swimport('dsp').dsp(URL,False)
  satellite=x.xpath('//div[@class="grid_3 alpha omega block"]/p/text()')
  branch=x.xpath('//div[@class="grid_6 alpha omega block"]/p/text()')
  save(["satellite"],[{"date_scraped":DATE,"satellite":clean(s),"branch":clean(b)} for (s,b) in zip(satellite,branch)],"final")

def clean(raw):
  return re.sub(whitespace_end,'',re.sub(whitespace_start,'',raw))

main()from scraperwiki.sqlite import save
from scraperwiki import swimport
import re
URL="http://www.landbank.co.za/contact/satellite_branches.php"
from time import time
DATE=time()

whitespace_start=re.compile(r'^[\t\n\r ]*')
whitespace_end=re.compile(r'[\t\n\r ]*$')

def main():
  x=swimport('dsp').dsp(URL,False)
  satellite=x.xpath('//div[@class="grid_3 alpha omega block"]/p/text()')
  branch=x.xpath('//div[@class="grid_6 alpha omega block"]/p/text()')
  save(["satellite"],[{"date_scraped":DATE,"satellite":clean(s),"branch":clean(b)} for (s,b) in zip(satellite,branch)],"final")

def clean(raw):
  return re.sub(whitespace_end,'',re.sub(whitespace_start,'',raw))

main()