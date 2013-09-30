require 'nokogiri'
require 'open-uri'

# html = ScraperWiki::scrape("http://index.museum/fullindex.php")           
html = open("http://index.museum/fullindex.php").read

doc = Nokogiri::HTML(html)

rows = doc.css("tr")
puts rows.size

rows.each do |row|
  begin
    url, name = row.css("td").map { |x| x.text.strip }
    url = "http://" + url
    ScraperWiki::save_sqlite(['url'], { url:url, name:name} ) 
  rescue
    puts "Error with #{name}"
    ScraperWiki::save_sqlite(['url'], { url:url, name:"UNREADABLE" } ) 
  end
end
require 'nokogiri'
require 'open-uri'

# html = ScraperWiki::scrape("http://index.museum/fullindex.php")           
html = open("http://index.museum/fullindex.php").read

doc = Nokogiri::HTML(html)

rows = doc.css("tr")
puts rows.size

rows.each do |row|
  begin
    url, name = row.css("td").map { |x| x.text.strip }
    url = "http://" + url
    ScraperWiki::save_sqlite(['url'], { url:url, name:name} ) 
  rescue
    puts "Error with #{name}"
    ScraperWiki::save_sqlite(['url'], { url:url, name:"UNREADABLE" } ) 
  end
end
