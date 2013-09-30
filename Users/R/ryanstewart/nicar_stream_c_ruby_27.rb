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

for tr in trs[0..3]
  tds = tr.search('td')
  cell_values = tds.map {|td| td.text}
  puts cell_values.zip(COLUMN_NAMES)
end



  [
      'employer','download','location','union',
      'local', 'naics', 'num_workers', 'expiration_date'
  ]

  
[
  ['employer', 'California  Processors Inc.\r\n    ',],
  ['download', 'Not Available'],
  
]require 'scraperwiki'
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

for tr in trs[0..3]
  tds = tr.search('td')
  cell_values = tds.map {|td| td.text}
  puts cell_values.zip(COLUMN_NAMES)
end



  [
      'employer','download','location','union',
      'local', 'naics', 'num_workers', 'expiration_date'
  ]

  
[
  ['employer', 'California  Processors Inc.\r\n    ',],
  ['download', 'Not Available'],
  
]