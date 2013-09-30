require 'nokogiri'
require 'scraperwiki'
require 'csv'
require 'mechanize'
require "net/http"
require "uri"

input = ScraperWiki::scrape("http://www.virginisles.com/urlsE1.csv") 

csv = CSV.new(input)
puts "Got the CSV"

for row in csv  
  puts "Now scraping #{row[0]}"
  uri = URI.parse(row[0])
  response = Net::HTTP.get_response(uri)
  puts "Response code is #{response.code}"
  if response.code.to_i == 200
    puts "Valid response for #{row[0]}"
    agent = Mechanize.new
    html = agent.get(row[0])
    data = html.search('p.wbThis a')
    url = data[0].content.to_s
    date = data[1].content.to_s
    p url
    p date
    ScraperWiki::save_sqlite(unique_keys=["url"], data={ "url" => url, "date" => date })
  else
    url = row[0]
    puts "Bad response for #{url}"
    date = response.code
    ScraperWiki::save_sqlite(unique_keys=["url"], data={ "url" => url, "date" => date })
  end   
end
require 'nokogiri'
require 'scraperwiki'
require 'csv'
require 'mechanize'
require "net/http"
require "uri"

input = ScraperWiki::scrape("http://www.virginisles.com/urlsE1.csv") 

csv = CSV.new(input)
puts "Got the CSV"

for row in csv  
  puts "Now scraping #{row[0]}"
  uri = URI.parse(row[0])
  response = Net::HTTP.get_response(uri)
  puts "Response code is #{response.code}"
  if response.code.to_i == 200
    puts "Valid response for #{row[0]}"
    agent = Mechanize.new
    html = agent.get(row[0])
    data = html.search('p.wbThis a')
    url = data[0].content.to_s
    date = data[1].content.to_s
    p url
    p date
    ScraperWiki::save_sqlite(unique_keys=["url"], data={ "url" => url, "date" => date })
  else
    url = row[0]
    puts "Bad response for #{url}"
    date = response.code
    ScraperWiki::save_sqlite(unique_keys=["url"], data={ "url" => url, "date" => date })
  end   
end
