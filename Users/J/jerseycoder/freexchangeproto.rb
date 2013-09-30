# Blank Ruby
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
          "date_end"=>"2011-06-05",
          "resultsperpage"=>"3"
      })
  response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}
  doc = Nokogiri::HTML.parse(response.body)
  info = ""
  doc.search('td').each do |td|
    info = info + td.text
  end
  print info
# Blank Ruby
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
          "date_end"=>"2011-06-05",
          "resultsperpage"=>"3"
      })
  response = Net::HTTP.new(url.host, url.port).start {|http| http.request(request)}
  doc = Nokogiri::HTML.parse(response.body)
  info = ""
  doc.search('td').each do |td|
    info = info + td.text
  end
  print info
