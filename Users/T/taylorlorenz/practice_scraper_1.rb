require 'scraperwiki'
require 'open-uri'
require 'nokogiri'

COLNAMES=['state','pop','rank']

def parseTable(url,population_subset)
  download = open(url)
  
  html = Nokogiri::HTML(download)
  tables = html.search('table')
  table = tables[0]
  
  trs = table.search('tr')
  
  trs.shift
  for tr in trs
    cells = tr.search('*')
    values = cells.map{|cell| cell.text}
    data = Hash[COLNAMES.zip(values)]
    if url=='http://www.census.gov/compendia/statab/2012/ranks/rank01.html'
      d=data['pop'].gsub(',','')
      data['pop']=Integer(d)
    else
      data['percent']=Float(data['pop'])
    end
    data['population_subset']=population_subset
    data['url']=url
    if data['rank']!='(X)'
      ScraperWiki.save([],data)
    end
  end
end

parseTable('http://www.census.gov/compendia/statab/2012/ranks/rank01.html','total')
parseTable('http://www.census.gov/compendia/statab/2012/ranks/rank03.html','under18')
parseTable('http://www.census.gov/compendia/statab/2012/ranks/rank04.html','under65')

require 'scraperwiki'
require 'open-uri'
require 'nokogiri'

COLNAMES=['state','pop','rank']

def parseTable(url,population_subset)
  download = open(url)
  
  html = Nokogiri::HTML(download)
  tables = html.search('table')
  table = tables[0]
  
  trs = table.search('tr')
  
  trs.shift
  for tr in trs
    cells = tr.search('*')
    values = cells.map{|cell| cell.text}
    data = Hash[COLNAMES.zip(values)]
    if url=='http://www.census.gov/compendia/statab/2012/ranks/rank01.html'
      d=data['pop'].gsub(',','')
      data['pop']=Integer(d)
    else
      data['percent']=Float(data['pop'])
    end
    data['population_subset']=population_subset
    data['url']=url
    if data['rank']!='(X)'
      ScraperWiki.save([],data)
    end
  end
end

parseTable('http://www.census.gov/compendia/statab/2012/ranks/rank01.html','total')
parseTable('http://www.census.gov/compendia/statab/2012/ranks/rank03.html','under18')
parseTable('http://www.census.gov/compendia/statab/2012/ranks/rank04.html','under65')

