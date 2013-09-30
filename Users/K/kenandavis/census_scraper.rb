require 'open-uri'
require 'scraperwiki'
require 'nokogiri'

COLNAMES = [
    'state','percent','rank'
]

URL='http://www.census.gov/compendia/statab/2012/ranks/rank04.html'

download = open(URL)
#puts download.read

page = Nokogiri::HTML(download)
table = page.search('table')

trs = table.search('tr')

trs.shift
for row in trs
  cells = row.search('*')
  values = cells.map{|cell| cell.text()}
  data = Hash[COLNAMES.zip(values)]
  #puts data
  data['percent'] = Float(data['percent'])
  
  if data['rank'] == '(X)'
    data['rank'] = 'unknown'
  else
    data['rank'] = Integer(data['rank'])
  end
  puts data
  ScraperWiki.save([],data)
endrequire 'open-uri'
require 'scraperwiki'
require 'nokogiri'

COLNAMES = [
    'state','percent','rank'
]

URL='http://www.census.gov/compendia/statab/2012/ranks/rank04.html'

download = open(URL)
#puts download.read

page = Nokogiri::HTML(download)
table = page.search('table')

trs = table.search('tr')

trs.shift
for row in trs
  cells = row.search('*')
  values = cells.map{|cell| cell.text()}
  data = Hash[COLNAMES.zip(values)]
  #puts data
  data['percent'] = Float(data['percent'])
  
  if data['rank'] == '(X)'
    data['rank'] = 'unknown'
  else
    data['rank'] = Integer(data['rank'])
  end
  puts data
  ScraperWiki.save([],data)
end