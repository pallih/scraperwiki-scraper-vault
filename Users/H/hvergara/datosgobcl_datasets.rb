require 'open-uri'
require 'nokogiri'

PAGE_URL = "http://www.data.gob.cl/datasets/listar?offset=%d&order_by=maestro.publicado_at%%20desc"

start_page = 0
per_page = 10

page = 0

loop do

  url = PAGE_URL % (page * per_page)
  html = open(url)
  
  
  doc = Nokogiri::HTML(html)
  items = doc.search("#tableDatasets h3 a")

  break if items.length == 0
  
  items.each do |item|
    title = item.inner_text.gsub(/\.?\s\(.*\)/, '').strip

    dataset = { :href => item['href'], :title => title }
    ScraperWiki::save_sqlite(unique_keys=[:href], data=dataset, table_name='datasets')
  end

  page += 1

end
require 'open-uri'
require 'nokogiri'

PAGE_URL = "http://www.data.gob.cl/datasets/listar?offset=%d&order_by=maestro.publicado_at%%20desc"

start_page = 0
per_page = 10

page = 0

loop do

  url = PAGE_URL % (page * per_page)
  html = open(url)
  
  
  doc = Nokogiri::HTML(html)
  items = doc.search("#tableDatasets h3 a")

  break if items.length == 0
  
  items.each do |item|
    title = item.inner_text.gsub(/\.?\s\(.*\)/, '').strip

    dataset = { :href => item['href'], :title => title }
    ScraperWiki::save_sqlite(unique_keys=[:href], data=dataset, table_name='datasets')
  end

  page += 1

end
