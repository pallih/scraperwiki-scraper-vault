require 'nokogiri'

html = ScraperWiki::scrape("http://scraperwiki.com/")
doc = Nokogiri::HTML(html)

doc.css('a').each do |link|
  ScraperWiki::save_sqlite(['href'], {class: link.class.to_s, href: link['href']})
end
