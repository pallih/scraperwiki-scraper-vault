# RSS Events Calendar

require 'open-uri'
require 'nokogiri'
require 'cgi'

url = 'http://www.trumba.com/calendars/public-event-ongoing.rss'
html = Nokogiri::XML(open(url))

html.css('item').each do |item|
  description = CGI.unescapeHTML(item.css('description').inner_html)
record = {'title' => item.css('title').inner_html, 'description' => description.gsub(/<|>|&nbsp;|:&nbsp;|nbsp;|&amp;|<br\/>|br\//, ''), 'date' => item.css('category').inner_html, 'link' => item.css('link').inner_html, 'publication_date' => item.css('pubDate').inner_html}
  
  description.scan(/<b>(.*?)<\/b>(.*?)<br\s?\/>/).each do |keyvalue|
    key = keyvalue[0].gsub(/\W/, '_').downcase
    if /href/.match(keyvalue[1])
record[key] = keyvalue[1].gsub(/&nbsp;|nbsp;|&amp;|:&amp;|<br\s?\/>|br\s?\//, '')
    else
record[key] = keyvalue[1].gsub(/&.{0,3};|&nbsp;|:&nbsp;|nbsp;|:&amp;|&amp;|br\s?\/|<br\s?\/>|br\s\//, '')
    end
  end

  ScraperWiki.save(record.keys, record)
end
