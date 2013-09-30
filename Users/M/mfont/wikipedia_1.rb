# Ruby



html = ScraperWiki.scrape "http://www.rfef.es/index.jsp?nodo=92&division=LIGA%20NACIONAL%20PRIMERA%20DIVISION&grupo=GRUPO%20UNICO&temporada=2010/2011%23%231"

require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search('title').each do |title|
  p title.inner_html
end

doc.search('table.findResult tr').each do |tr|
  puts tr.to_html
end

ScraperWiki.save_sqlite(unique_keys=['tr'], data=data)    # Ruby



html = ScraperWiki.scrape "http://www.rfef.es/index.jsp?nodo=92&division=LIGA%20NACIONAL%20PRIMERA%20DIVISION&grupo=GRUPO%20UNICO&temporada=2010/2011%23%231"

require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search('title').each do |title|
  p title.inner_html
end

doc.search('table.findResult tr').each do |tr|
  puts tr.to_html
end

ScraperWiki.save_sqlite(unique_keys=['tr'], data=data)    