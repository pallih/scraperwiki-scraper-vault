# Blank Ruby
require 'nokogiri'

BASE = 'http://www.cymdeithaswaldosociety.org.uk'
html = ScraperWiki.scrape BASE

doc = Nokogiri::HTML(html)
doc.xpath('//ul[@class="wsite-menu"]//li/a').each do |link|
  href = link['href']
  if href =~ /^\//
    target = BASE + href
  else 
    target = href
  end
  content = ScraperWiki.scrape target
  content_doc = Nokogiri::HTML(content)
  titles = content_doc.search('title')
  title = titles.inner_html
  clipped_title = title[/[^-]+/].strip
  bodies = content_doc.search('div#wsite-content')
  body = bodies.inner_html
  data = {
    'id' => href,
    'title' => clipped_title,
    'body' => body
  }
  data.each {|key,val| val.encode!('UTF-8')}
  ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
end