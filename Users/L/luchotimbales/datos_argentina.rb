# Ruby script that grabs data from argentinian government website

$url= ""

html= ScraperWiki.scrape($url)
puts html

require 'nokogiri'
    
doc = Nokogiri::HTML(html)
doc.search('a').each do |link|
  $url=link.attr("href")
  puts $url
  $url=URI.parse(URI.encode($url.strip))
  html= ScraperWiki.scrape($url)
  puts html
  
  record = {}        
  record['URL']= $url
  record['html'] = html
  ScraperWiki.save_sqlite(["URL"], record)
  
end

# Ruby script that grabs data from argentinian government website

$url= ""

html= ScraperWiki.scrape($url)
puts html

require 'nokogiri'
    
doc = Nokogiri::HTML(html)
doc.search('a').each do |link|
  $url=link.attr("href")
  puts $url
  $url=URI.parse(URI.encode($url.strip))
  html= ScraperWiki.scrape($url)
  puts html
  
  record = {}        
  record['URL']= $url
  record['html'] = html
  ScraperWiki.save_sqlite(["URL"], record)
  
end

# Ruby script that grabs data from argentinian government website

$url= ""

html= ScraperWiki.scrape($url)
puts html

require 'nokogiri'
    
doc = Nokogiri::HTML(html)
doc.search('a').each do |link|
  $url=link.attr("href")
  puts $url
  $url=URI.parse(URI.encode($url.strip))
  html= ScraperWiki.scrape($url)
  puts html
  
  record = {}        
  record['URL']= $url
  record['html'] = html
  ScraperWiki.save_sqlite(["URL"], record)
  
end

