require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://bctransit.com/'

Nokogiri::HTML(open(BASE_URL), nil, 'ISO-8859-1').css('.custalert').each do |alertMatch|
  if alertMatch.at_css('h1').content.downcase.match(/victoria/)
    puts alertMatch
  end
end
