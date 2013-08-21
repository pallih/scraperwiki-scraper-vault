require 'scraperwiki'
require 'open-uri'
require 'nokogiri'

#List of column names
COLUMN_NAMES = [
  'employer','download','location','union',
  'local', 'naics', 'num_workers', 'expiration_date'
]

download = open('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
html = Nokogiri::HTML(download)
tables = html.search('table')
table = tables[2]

trs = table.search('tr')

trs.shift

for tr in trs
  tds = tr.search('td')
  cell_values = tds.map {|td| td.text}
  data = Hash[COLUMN_NAMES.zip(cell_values)]
  ScraperWiki.save([], data)
end