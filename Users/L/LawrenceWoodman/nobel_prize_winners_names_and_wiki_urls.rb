require 'nokogiri' 

html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/Nobel_prize_winners")

winners = {}
doc = Nokogiri::HTML(html)
doc.css('table.wikitable td span.fn a').each do |a|
  name = a.inner_text
  wiki_url = a.attribute('href')
  absolute_url = "http://wikipedia.org#{wiki_url}"
  winners[absolute_url] = name
end

# Save data to database
winners.each do |url, name|
  data = {
    'url' => url,
    'name' => name
  }
  ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
endrequire 'nokogiri' 

html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/Nobel_prize_winners")

winners = {}
doc = Nokogiri::HTML(html)
doc.css('table.wikitable td span.fn a').each do |a|
  name = a.inner_text
  wiki_url = a.attribute('href')
  absolute_url = "http://wikipedia.org#{wiki_url}"
  winners[absolute_url] = name
end

# Save data to database
winners.each do |url, name|
  data = {
    'url' => url,
    'name' => name
  }
  ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
end