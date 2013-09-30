##adapted from Max Ogden's tutorial SW code @ https://gist.github.com/727674
#&
##kludged together with https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1

require 'net/http'
require 'uri'
require 'nokogiri'

def testing()

url = URI.parse('http://locator.moneypass.com/searchresults.aspx')

request = Net::HTTP::Post.new(url.path)

request.set_form_data({"distance"=>"20",
                       "typeofloc"=>"ALL",
                       "street"=>"",
                       "city"=>"Detroit",
                       "state"=>"MI",
                       "zipcode"=>"",
                       "country"=>"",
                       "institutionName"=>"",
                       "latitude"=>"42.33168",
                       "longitude"=>"-83.04792"})

response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}

doc = Nokogiri::HTML.parse(response.body)

##scrapes a bit messy, but gets all the place names and addresses for at least the first page

  doc.search('#DataGrid1 td').each do |hailMary|
    info = hailMary.text.each_line.map(&:strip).delete_if {|l| l.strip==""}.join(',')
    ScraperWiki.save(unique_keys=['text'], data = {'text'=> info})
  end
end

testing()
##TODO: get script to plow through ASP.net pagination until all the data is scraped##adapted from Max Ogden's tutorial SW code @ https://gist.github.com/727674
#&
##kludged together with https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1

require 'net/http'
require 'uri'
require 'nokogiri'

def testing()

url = URI.parse('http://locator.moneypass.com/searchresults.aspx')

request = Net::HTTP::Post.new(url.path)

request.set_form_data({"distance"=>"20",
                       "typeofloc"=>"ALL",
                       "street"=>"",
                       "city"=>"Detroit",
                       "state"=>"MI",
                       "zipcode"=>"",
                       "country"=>"",
                       "institutionName"=>"",
                       "latitude"=>"42.33168",
                       "longitude"=>"-83.04792"})

response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}

doc = Nokogiri::HTML.parse(response.body)

##scrapes a bit messy, but gets all the place names and addresses for at least the first page

  doc.search('#DataGrid1 td').each do |hailMary|
    info = hailMary.text.each_line.map(&:strip).delete_if {|l| l.strip==""}.join(',')
    ScraperWiki.save(unique_keys=['text'], data = {'text'=> info})
  end
end

testing()
##TODO: get script to plow through ASP.net pagination until all the data is scraped##adapted from Max Ogden's tutorial SW code @ https://gist.github.com/727674
#&
##kludged together with https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1

require 'net/http'
require 'uri'
require 'nokogiri'

def testing()

url = URI.parse('http://locator.moneypass.com/searchresults.aspx')

request = Net::HTTP::Post.new(url.path)

request.set_form_data({"distance"=>"20",
                       "typeofloc"=>"ALL",
                       "street"=>"",
                       "city"=>"Detroit",
                       "state"=>"MI",
                       "zipcode"=>"",
                       "country"=>"",
                       "institutionName"=>"",
                       "latitude"=>"42.33168",
                       "longitude"=>"-83.04792"})

response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}

doc = Nokogiri::HTML.parse(response.body)

##scrapes a bit messy, but gets all the place names and addresses for at least the first page

  doc.search('#DataGrid1 td').each do |hailMary|
    info = hailMary.text.each_line.map(&:strip).delete_if {|l| l.strip==""}.join(',')
    ScraperWiki.save(unique_keys=['text'], data = {'text'=> info})
  end
end

testing()
##TODO: get script to plow through ASP.net pagination until all the data is scraped##adapted from Max Ogden's tutorial SW code @ https://gist.github.com/727674
#&
##kludged together with https://scraperwiki.com/scrapers/advanced-scraping-aspx-pages-1

require 'net/http'
require 'uri'
require 'nokogiri'

def testing()

url = URI.parse('http://locator.moneypass.com/searchresults.aspx')

request = Net::HTTP::Post.new(url.path)

request.set_form_data({"distance"=>"20",
                       "typeofloc"=>"ALL",
                       "street"=>"",
                       "city"=>"Detroit",
                       "state"=>"MI",
                       "zipcode"=>"",
                       "country"=>"",
                       "institutionName"=>"",
                       "latitude"=>"42.33168",
                       "longitude"=>"-83.04792"})

response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}

doc = Nokogiri::HTML.parse(response.body)

##scrapes a bit messy, but gets all the place names and addresses for at least the first page

  doc.search('#DataGrid1 td').each do |hailMary|
    info = hailMary.text.each_line.map(&:strip).delete_if {|l| l.strip==""}.join(',')
    ScraperWiki.save(unique_keys=['text'], data = {'text'=> info})
  end
end

testing()
##TODO: get script to plow through ASP.net pagination until all the data is scraped