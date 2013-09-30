import scraperwiki

# Blank Python
# require 'nokogiri'
html = ScraperWiki::scrape("https://scraperwiki.com/")
doc = Nokogiri::HTML(html)
doc.css('div.featured a').each do |link|
  puts link.class
end
  puts link.to_html
import scraperwiki

# Blank Python
# require 'nokogiri'
html = ScraperWiki::scrape("https://scraperwiki.com/")
doc = Nokogiri::HTML(html)
doc.css('div.featured a').each do |link|
  puts link.class
end
  puts link.to_html
