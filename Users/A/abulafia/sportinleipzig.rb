require 'nokogiri'

url = "http://www.sportinleipzig.de/Verzeichnis/Sport/id,18+Judo/"

html = ScraperWiki.scrape(url)

doc = Nokogiri::HTML(html)

rows = doc.css('div.contentbox table tbody tr') 

rows.each do |row|
  weekday  = row.xpath('.//td[3]').text
  time     = row.xpath('./td[4]').text
  location = row.xpath('./td[6]/a').text

  id = row.attribute('id').text
  id = id.gsub('tr_', '').to_i
  
  result = {
    'id'       => id,
    'weekday'  => weekday,
    'time'     => time,
    'location' => location
  }

  ScraperWiki.save_sqlite(unique_keys=['id'], result)

end
require 'nokogiri'

url = "http://www.sportinleipzig.de/Verzeichnis/Sport/id,18+Judo/"

html = ScraperWiki.scrape(url)

doc = Nokogiri::HTML(html)

rows = doc.css('div.contentbox table tbody tr') 

rows.each do |row|
  weekday  = row.xpath('.//td[3]').text
  time     = row.xpath('./td[4]').text
  location = row.xpath('./td[6]/a').text

  id = row.attribute('id').text
  id = id.gsub('tr_', '').to_i
  
  result = {
    'id'       => id,
    'weekday'  => weekday,
    'time'     => time,
    'location' => location
  }

  ScraperWiki.save_sqlite(unique_keys=['id'], result)

end
