# RSS Events Calendar

require 'open-uri'
require 'nokogiri'
require 'cgi'

url = 'http://www.trumba.com/calendars/seattlegov-city-wide.rss'
html = Nokogiri::XML(open(url))

html.css('item').each do |item|
record = {
  'item' => item.css('title').inner_html,
  'date' => item.css('category').inner_html,
  'link' => item.css('link').inner_html,
  'publication_date' => item.css('pubDate').inner_html}
  description = item.css('description').inner_html
  unescapedDescription = CGI.unescapeHTML(description)
  splitDescription = unescapedDescription.split('<br/><br/>')
  record["description"] = splitDescription[0 .. -2].join('<br/><br/>')
  fields = splitDescription.last
  splitFields = fields.split('<br/>')


  mappedFields = splitFields.map{|field| field.match(/<b>(.*)<\/b>:&nbsp;(.*)/)}
  
  mappedFields.each do |field|
    record[field[1]] = field[2]
  end

  # Attempting shorter version
  #mappedFields = splitFields.map{|field| field.match(/<b>(.*)<\/b>:&nbsp;(.*)/)[1..2]}
  #h=Hash[*mappedFields.flatten]
  #record.merge h

  ScraperWiki.save(record.keys, record)
end
# RSS Events Calendar

require 'open-uri'
require 'nokogiri'
require 'cgi'

url = 'http://www.trumba.com/calendars/seattlegov-city-wide.rss'
html = Nokogiri::XML(open(url))

html.css('item').each do |item|
record = {
  'item' => item.css('title').inner_html,
  'date' => item.css('category').inner_html,
  'link' => item.css('link').inner_html,
  'publication_date' => item.css('pubDate').inner_html}
  description = item.css('description').inner_html
  unescapedDescription = CGI.unescapeHTML(description)
  splitDescription = unescapedDescription.split('<br/><br/>')
  record["description"] = splitDescription[0 .. -2].join('<br/><br/>')
  fields = splitDescription.last
  splitFields = fields.split('<br/>')


  mappedFields = splitFields.map{|field| field.match(/<b>(.*)<\/b>:&nbsp;(.*)/)}
  
  mappedFields.each do |field|
    record[field[1]] = field[2]
  end

  # Attempting shorter version
  #mappedFields = splitFields.map{|field| field.match(/<b>(.*)<\/b>:&nbsp;(.*)/)[1..2]}
  #h=Hash[*mappedFields.flatten]
  #record.merge h

  ScraperWiki.save(record.keys, record)
end
