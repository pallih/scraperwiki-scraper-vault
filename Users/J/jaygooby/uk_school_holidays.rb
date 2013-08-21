# Given a UK school URN like 114377 (Stanford Infants, Brighton, East Sussex)
# extract the holidays for the year for the school

require 'nokogiri' 
require 'yaml'

html = ScraperWiki.scrape("http://myschoolholidays.com/school.php?id=114377")
doc = Nokogiri::HTML(html)

js = doc.css('.half-left222').at('script').text

puts "js: #{js}"

holidays = js.scan(/var holidays = (.*);/).flatten[0].to_s
puts "holidays: #{holidays}"

dates = holidays.gsub!(/(\,)(\S)/, "\\1 \\2")

puts dates

date_array = YAML::load(holidays)

puts "dates: #{date_array[0]}"
