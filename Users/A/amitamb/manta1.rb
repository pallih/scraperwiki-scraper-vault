html = ScraperWiki::scrape("http://www.manta.com/world/Asia/Turkey/")           

puts html

require 'nokogiri'           
doc = Nokogiri::HTML html
doc.css(".results-area .box a.mb_browse_link").each do |v|
  # puts v
  puts v
  if v[:href] && v[:href].match(/^http\:\/\/www\.manta\.com\/world\/Asia\/Turkey\/\-\//) 
  puts v[:href]
  end
end