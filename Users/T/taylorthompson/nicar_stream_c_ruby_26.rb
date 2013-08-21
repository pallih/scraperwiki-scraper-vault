require 'scraperwiki'
require 'open-uri'
require 'nokogiri'

download = open('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
html = Nokogiri::HTML(download)
tables = html.search('table')
table = tables[2]

trs = table.search('tr')
tr = trs[6] #Replace this line
for tr in trs #finish this line
  tds = tr.search('td')
  for td in tds
    puts td.text
  end
end