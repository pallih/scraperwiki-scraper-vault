require 'nokogiri'
require 'json'
base = 'http://rosecityresource.org'
html = ScraperWiki.scrape(base + '/map')
markers = JSON.parse(html.split('"markers":')[1].split('} } } });')[0])
markers.each do |marker|
  info = Nokogiri::HTML.parse(marker['text'].gsub("x3c", "<").gsub("x3e", ">"))
  link = info.css('a').attr('href').value
  name = info.css('a').attr('title').value
  page = Nokogiri::HTML.parse(ScraperWiki.scrape(base + link))
  english = page.css('.node_translation_en')
  if english.length > 0
    page = Nokogiri::HTML.parse(ScraperWiki.scrape(base + english.css('a').attr('href').value))
  end
  website = page.css('.field-field-website').attr('href').value rescue ""
  details = {
    "name" => name,
    "link" => link,
    "website" => website,
    "text" => page.css('.field-field-phone').text,
    "timestamp" => page.css('.submitted').text,
    "hours" => page.css('.field-field-hours').text,
    "description" => page.css('.content p').text,
    "latitude" => marker['latitude'],
    "longitude" => marker['longitude']
  }
  p details
  ScraperWiki.save_sqlite(unique_keys=["link"], data=details)
end