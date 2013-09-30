require 'scraperwiki'
require 'open-uri'
require 'nokogiri'

download = open('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
html = Nokogiri::HTML(download)
tables = html.search('table')
puts tablesrequire 'scraperwiki'
require 'open-uri'
require 'nokogiri'

download = open('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
html = Nokogiri::HTML(download)
tables = html.search('table')
puts tables