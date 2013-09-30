require 'net/http'
require 'uri'
require 'nokogiri'

url = URI.parse('http://groups.freecycle.org/oaklandfreecycle/posts/search?search_words=couch&include_offers=on&include_wanteds=on&date_start=&date_end=&resultsperpage=10')

request = Net::HTTP::Post.new(url.path)

request.set_form_data({
  "REST"=>" ",
  "STR_NBR"=>"",
  "STR_NBR2"=>"",
  "STR_DIRECTION"=>"",
  "STR_NM"=>"",
  "ZIP"=>""
})

response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}

doc = Nokogiri::HTML.parse(response.body)

doc.search('#results tr').each do |tr|
  info = tr.text.each_line.map(&:strip).delete_if {|l| l.strip == ""}.join('\n')
  ScraperWiki.save(unique_keys=['text'], data = {'text' => info})
endrequire 'net/http'
require 'uri'
require 'nokogiri'

url = URI.parse('http://groups.freecycle.org/oaklandfreecycle/posts/search?search_words=couch&include_offers=on&include_wanteds=on&date_start=&date_end=&resultsperpage=10')

request = Net::HTTP::Post.new(url.path)

request.set_form_data({
  "REST"=>" ",
  "STR_NBR"=>"",
  "STR_NBR2"=>"",
  "STR_DIRECTION"=>"",
  "STR_NM"=>"",
  "ZIP"=>""
})

response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}

doc = Nokogiri::HTML.parse(response.body)

doc.search('#results tr').each do |tr|
  info = tr.text.each_line.map(&:strip).delete_if {|l| l.strip == ""}.join('\n')
  ScraperWiki.save(unique_keys=['text'], data = {'text' => info})
end