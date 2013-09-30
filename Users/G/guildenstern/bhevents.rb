require 'open-uri'
require 'nokogiri'
require 'scraperwiki'

url = "http://berghain.de/events"

html = URI.parse(url).read
puts "Read document"

doc = Nokogiri::HTML html
#ScraperWiki::sqliteexecute("drop table swdata") 
doc.search("div.col").each do |div|
  vs = {}
  div.search('h4').each do |v|
    a = v.search("a").first
    href = a['href']
    vs[:id] = href.split("/").last.to_i
    vs[:href] = href

    date, vs[:title] = v.text.to_s.strip.split(/\s\s+/)
    vs[:date] = Date.parse date
    vs[:type] = v['class'].gsub("type_", '')
  end
  content =  div.search("p span").first
  puts
  puts "=======" + vs[:title]
  descr = {}
  content.search("b").each do |b|
    descr[b.text] = b.next_sibling.text.strip.split(",").map(&:strip)
  end
  vs[:artists] = descr

  event_url = "http://berghain.de" + vs[:href]
  puts event_url  
  event_html = URI.parse(event_url).read
  event_doc = Nokogiri::HTML event_html
  tt = event_doc.search(".col_context").first.inner_html.strip
  vs[:timetable] = tt
  ScraperWiki::save_sqlite(unique_keys=[:id], data=vs)
end



require 'open-uri'
require 'nokogiri'
require 'scraperwiki'

url = "http://berghain.de/events"

html = URI.parse(url).read
puts "Read document"

doc = Nokogiri::HTML html
#ScraperWiki::sqliteexecute("drop table swdata") 
doc.search("div.col").each do |div|
  vs = {}
  div.search('h4').each do |v|
    a = v.search("a").first
    href = a['href']
    vs[:id] = href.split("/").last.to_i
    vs[:href] = href

    date, vs[:title] = v.text.to_s.strip.split(/\s\s+/)
    vs[:date] = Date.parse date
    vs[:type] = v['class'].gsub("type_", '')
  end
  content =  div.search("p span").first
  puts
  puts "=======" + vs[:title]
  descr = {}
  content.search("b").each do |b|
    descr[b.text] = b.next_sibling.text.strip.split(",").map(&:strip)
  end
  vs[:artists] = descr

  event_url = "http://berghain.de" + vs[:href]
  puts event_url  
  event_html = URI.parse(event_url).read
  event_doc = Nokogiri::HTML event_html
  tt = event_doc.search(".col_context").first.inner_html.strip
  vs[:timetable] = tt
  ScraperWiki::save_sqlite(unique_keys=[:id], data=vs)
end



