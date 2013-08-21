# number of calculatable digits using pentium CPU
puts RUBY_DESCRIPTION
require 'nokogiri'

url = 'http://ja.uncyclopedia.info/wiki/Pentium'

doc = Nokogiri::HTML(ScraperWiki.scrape(url))
digits = doc.search('p').select{|x| x.inner_text.match /桁/ }.map do |x|
  record = { 
    #:cpu_name => x.,
    :doc_with_digit => x.inner_text.split("。").select{|x| x.match(/桁/)}.first,
  }
  puts record
end
