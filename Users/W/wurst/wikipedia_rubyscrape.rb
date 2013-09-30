# Blank Ruby
require 'nokogiri'

#require 'rubygems'
#require 'mechanize'

#a = Mechanize.new {}

#html = a.get('http://en.wikipedia.org/wiki/List_of_modern_dictators')

page = Nokogiri::HTML(open('http://en.wikipedia.org/wiki/List_of_modern_dictators'))
page.css('table:nth-of-type(2) tr').each do |akwZeile|
  akw_cell = akwZeile.css('td')
  if (!akw_cell.empty?)
    akwData = {
      'power' => akw_cell[0].child.content,
    }
    puts akwData
    unique_keys = ['power']
    ScraperWiki.save_sqlite(unique_keys, akwData)
  end
end
# Blank Ruby
require 'nokogiri'

#require 'rubygems'
#require 'mechanize'

#a = Mechanize.new {}

#html = a.get('http://en.wikipedia.org/wiki/List_of_modern_dictators')

page = Nokogiri::HTML(open('http://en.wikipedia.org/wiki/List_of_modern_dictators'))
page.css('table:nth-of-type(2) tr').each do |akwZeile|
  akw_cell = akwZeile.css('td')
  if (!akw_cell.empty?)
    akwData = {
      'power' => akw_cell[0].child.content,
    }
    puts akwData
    unique_keys = ['power']
    ScraperWiki.save_sqlite(unique_keys, akwData)
  end
end
