require 'open-uri'
require 'scraperwiki'
require 'nokogiri'

URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'

download = open(URL)
#puts download.read

steve = Nokogiri::HTML(download)
taylor = steve.search('table')
table = taylor[2]

jonathan = table.search('tr')

jon = jonathan[23].search('td, th')

bill = jon[4]
apple = bill.text()

puts apple