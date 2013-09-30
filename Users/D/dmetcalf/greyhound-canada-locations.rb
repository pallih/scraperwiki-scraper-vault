require 'nokogiri'

# retrieve a page
base_url = 'http://www.greyhound.ca/HOME/en/location/'
starting_url = base_url + 'locations.aspx?state=on&name=Ontario'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all links and assign to an array
doc = Nokogiri::HTML(html)
links = doc.search("td span a").to_ary
puts ("Number of stops: #{links.length}")

#remove all JavaScript from the array elements, leaving the URL stub and stop name
(0..links.length).each do |i|
  links[i] = links[i].to_s.gsub('"', '')
  links[i] = links[i].gsub("<a href=JavaScript:%20SpecialEventWin('/home/en/location/",'')
  links[i] = links[i].gsub("',%20'Location_Information',%20'700',%20'500')>",' ')
  links[i] = links[i].gsub("</a>",' ')
end

#delete all links that are just bus stops, not full bus locations
links.delete_if { |x| x.include? "BusStop" }
puts ("Number of full stops: #{links.length}")

#puts links[0][0,34]
#puts base_url + links[0][0,34]

(0..links.length).each do |i|
  stop_html = ScraperWiki.scrape(base_url + links[i][0,34])
  stop_page = Nokogiri::HTML(stop_html)
  postalcode = stop_page.to_s.scan(/[A-Z]\d[A-Z]\d[A-Z]\d/)
  #ScraperWiki.save(['Stop', 'Postal code'], 
  #  {'Stop' => links[i][35,99], 'Postal code' => postalcode })
  ScraperWiki.save(['Stop', 'PostalCode'], {'Stop' => links[i][35,99], 'PostalCode' => postalcode })
end

#print all elements of the array
#(0..links.length).each do |i|
#  puts ("links#{i}: #{links[i]}")
#end
require 'nokogiri'

# retrieve a page
base_url = 'http://www.greyhound.ca/HOME/en/location/'
starting_url = base_url + 'locations.aspx?state=on&name=Ontario'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all links and assign to an array
doc = Nokogiri::HTML(html)
links = doc.search("td span a").to_ary
puts ("Number of stops: #{links.length}")

#remove all JavaScript from the array elements, leaving the URL stub and stop name
(0..links.length).each do |i|
  links[i] = links[i].to_s.gsub('"', '')
  links[i] = links[i].gsub("<a href=JavaScript:%20SpecialEventWin('/home/en/location/",'')
  links[i] = links[i].gsub("',%20'Location_Information',%20'700',%20'500')>",' ')
  links[i] = links[i].gsub("</a>",' ')
end

#delete all links that are just bus stops, not full bus locations
links.delete_if { |x| x.include? "BusStop" }
puts ("Number of full stops: #{links.length}")

#puts links[0][0,34]
#puts base_url + links[0][0,34]

(0..links.length).each do |i|
  stop_html = ScraperWiki.scrape(base_url + links[i][0,34])
  stop_page = Nokogiri::HTML(stop_html)
  postalcode = stop_page.to_s.scan(/[A-Z]\d[A-Z]\d[A-Z]\d/)
  #ScraperWiki.save(['Stop', 'Postal code'], 
  #  {'Stop' => links[i][35,99], 'Postal code' => postalcode })
  ScraperWiki.save(['Stop', 'PostalCode'], {'Stop' => links[i][35,99], 'PostalCode' => postalcode })
end

#print all elements of the array
#(0..links.length).each do |i|
#  puts ("links#{i}: #{links[i]}")
#end
