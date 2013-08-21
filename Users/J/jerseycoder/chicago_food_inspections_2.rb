require 'net/http'
require 'uri'
require 'nokogiri'

url = URI.parse('http://groups.freecycle.org/oaklandfreecycle/posts/search?')

request = Net::HTTP::Post.new(url.path)

request.set_form_data({
  "search_words"=>"couch",
  "include_offers"=>"on",
  "include_wanteds"=>"off",
  "date_start"=>"2011-02-01",
  "date_end"=>"2011-06-04",
  "resultsperpage"=>"10"
})


response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}

doc = Nokogiri::HTML.parse(response.body)
#tds = parse.xpath("//td").text; 

doc.search('td').each do |td|
  #item = td.search('strong').text
  #date = td.search('').text
  info = td.text
  #date = td.xpath("//OutputGeocode/Longitude").text;
  #itemtitle = td. 
  
  ScraperWiki.save(unique_keys=['text'], data = {'text' => info})
end