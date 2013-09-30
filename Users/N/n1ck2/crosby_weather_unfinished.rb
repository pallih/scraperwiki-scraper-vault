# Blank Ruby
puts "Hello, coding in the (rain) cloud!"
html = ScraperWiki.scrape("http://www.metoffice.gov.uk/weather/uk/nw/crosby_latest_weather.html")
puts html
require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("div.tableWrapper") 

  cells = v.search('td')
  data = {
    'temp' => cells[3].inner_html,
    'wind speed' => cells[6].inner_html,
    'vis' => cells[10].inner_html,
    'pressure' => cells[12].inner_html.to_i
  }

  ScraperWiki.save_sqlite(unique_keys=['temp', 'wind speed', 'vis', 'pressure'], data=data)
  
end
# Blank Ruby
puts "Hello, coding in the (rain) cloud!"
html = ScraperWiki.scrape("http://www.metoffice.gov.uk/weather/uk/nw/crosby_latest_weather.html")
puts html
require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("div.tableWrapper") 

  cells = v.search('td')
  data = {
    'temp' => cells[3].inner_html,
    'wind speed' => cells[6].inner_html,
    'vis' => cells[10].inner_html,
    'pressure' => cells[12].inner_html.to_i
  }

  ScraperWiki.save_sqlite(unique_keys=['temp', 'wind speed', 'vis', 'pressure'], data=data)
  
end
