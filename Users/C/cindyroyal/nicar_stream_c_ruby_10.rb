require 'scraperwiki'

require 'open-uri'
require 'nokogiri'



download = open('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')

html = Nokogiri::HTML(download)
tables = html.search('table')
table = tables[2]

trs = table.search('tr')
tr= trs[6]

tds = tr.search('td')

for td in tds
  puts td.text
end

trs = table.search('tr')
for tr in trs
 puts tr.text
end




require 'scraperwiki'

require 'open-uri'
require 'nokogiri'



download = open('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')

html = Nokogiri::HTML(download)
tables = html.search('table')
table = tables[2]

trs = table.search('tr')
tr= trs[6]

tds = tr.search('td')

for td in tds
  puts td.text
end

trs = table.search('tr')
for tr in trs
 puts tr.text
end




