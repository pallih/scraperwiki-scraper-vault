html = ScraperWiki::scrape("http://www.northampton.ac.uk/events/full/20137")           
require 'nokogiri'           
doc = Nokogiri::HTML html
id=0
# Feed items on the page are wrapped in an a tag with the feed item URL.
# This doesn't have a class or ID, so we need to get it in a sloppy fashion:
doc.search("span.rsList a").each do |i|
  url=i.first[1]
  # The rest of the data can be accessed via the css method:
  data = {
    id: id,
    url: url,
    date: Time.now,
    title: i.css("span.entry-title").inner_html,
    description: i.css("span.lDate").inner_html + ': ' + i.css("span.entry-content").inner_html
  }
  ScraperWiki::save_sqlite(['id'], data) 
  id += 1
end


html = ScraperWiki::scrape("http://www.northampton.ac.uk/events/full/20137")           
require 'nokogiri'           
doc = Nokogiri::HTML html
id=0
# Feed items on the page are wrapped in an a tag with the feed item URL.
# This doesn't have a class or ID, so we need to get it in a sloppy fashion:
doc.search("span.rsList a").each do |i|
  url=i.first[1]
  # The rest of the data can be accessed via the css method:
  data = {
    id: id,
    url: url,
    date: Time.now,
    title: i.css("span.entry-title").inner_html,
    description: i.css("span.lDate").inner_html + ': ' + i.css("span.entry-content").inner_html
  }
  ScraperWiki::save_sqlite(['id'], data) 
  id += 1
end


