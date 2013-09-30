require 'nokogiri'
require 'open-uri'


# retrieve a page
base_url = 'http://www.viarail.ca/'
starting_url = base_url + 'en/stations/ontario/list'
#html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all links and assign to an array
# doc = Nokogiri::HTML(html)
doc = Nokogiri::HTML(open("http://www.viarail.ca/en/stations/ontario/list"))
links = doc.search("td div a").to_ary

puts ("Number of links: #{links.length}")


#convert all array elements to strings
links2 = []
(0..links.length-1).each do |i|
  links2[i] = links[i].to_s
end
puts ("Number of links2: #{links2.length}")

#delete all non-station array elements
links3 = []
links3 = links2.keep_if {|v| v.include? "/en/stations/ontario/"}
puts ("Number of links3: #{links3.length}")

#remove all cruft from the array elements, leaving the URL stub and stop name
links4 = []
(0..links3.length-1).each do |i|
  links4[i] = links3[i].gsub("<a href=",'')
  links4[i] = links4[i].gsub("</a>",' ')
  links4[i] = links4[i].gsub(">",' ')
  links4[i] = links4[i].gsub('"','')
  #puts ("Station #{i}: #{links4[i]}")
end
puts ("Number of links4: #{links4.length}")

station_url = "http://www.viarail.ca/en/stations/ontario/aldershot" 
station_html = Nokogiri::HTML(open(station_url))
puts station_html
station_html = station_html.search("td div div div script")
puts station_html
latitude = station_html.to_s
puts latitude
latitude.scan(/[4-5][0-9]\.[0-9][0-9][0-9][0-9]/)
puts latitude


#(0..links4.length-1).each do |i|
=begin
postalcode = []
(0..10).each do |i|
  space_location = links4[i].index(' ')
  #puts ("Station #{i} space location: #{space_location}")
  station_name = links4[i][space_location,links4[i].length]
  puts ("Station #{i} name: #{station_name}")
  station_url = base_url + links4[i][1,space_location-1]
  puts ("Station #{i} URL: #{station_url}")
  #station_html = ScraperWiki.scrape(station_url)
  station_html = Nokogiri::HTML(open(station_url))
  #puts ("Station #{i} HTML: #{station_html}")
  postalcode = station_html.search("td div div div div div").to_s.scan(/[A-Z]\d[A-Z] \d[A-Z]\d/)
  puts ("Station #{i} postal code: #{postalcode}")
  latitude = station_html.search("td div div div iframe").to_s.scan(/[4-5][0-9]\.[0-9][0-9][0-9][0-9]/)
  puts ("Station #{i} latitude: #{latitude}")
  longitude = station_html.search("td div div div iframe").to_s.scan(/[6-9][0-9]\.[0-9][0-9][0-9][0-9]/)
  if (!longitude.to_s.empty?)
    longitude = "-" + longitude.to_s
  end
  puts ("Station #{i} longitude: #{longitude}")
  #ScraperWiki.save(['Stop', 'Postal code'],
  #  {'Stop' => links[i][35,99], 'Postal code' => postalcode })
  ScraperWiki.save(['Station', 'PostalCode', 'Latitude', 'Longitude'], {'Station' => station_name, 'PostalCode' => postalcode, 'Latitude' => latitude, 'Longitude' => longitude })
end
=end

#print all elements of the array
#(0..links.length).each do |i|
#  puts ("links#{i}: #{links[i]}")
#end

require 'nokogiri'
require 'open-uri'


# retrieve a page
base_url = 'http://www.viarail.ca/'
starting_url = base_url + 'en/stations/ontario/list'
#html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all links and assign to an array
# doc = Nokogiri::HTML(html)
doc = Nokogiri::HTML(open("http://www.viarail.ca/en/stations/ontario/list"))
links = doc.search("td div a").to_ary

puts ("Number of links: #{links.length}")


#convert all array elements to strings
links2 = []
(0..links.length-1).each do |i|
  links2[i] = links[i].to_s
end
puts ("Number of links2: #{links2.length}")

#delete all non-station array elements
links3 = []
links3 = links2.keep_if {|v| v.include? "/en/stations/ontario/"}
puts ("Number of links3: #{links3.length}")

#remove all cruft from the array elements, leaving the URL stub and stop name
links4 = []
(0..links3.length-1).each do |i|
  links4[i] = links3[i].gsub("<a href=",'')
  links4[i] = links4[i].gsub("</a>",' ')
  links4[i] = links4[i].gsub(">",' ')
  links4[i] = links4[i].gsub('"','')
  #puts ("Station #{i}: #{links4[i]}")
end
puts ("Number of links4: #{links4.length}")

station_url = "http://www.viarail.ca/en/stations/ontario/aldershot" 
station_html = Nokogiri::HTML(open(station_url))
puts station_html
station_html = station_html.search("td div div div script")
puts station_html
latitude = station_html.to_s
puts latitude
latitude.scan(/[4-5][0-9]\.[0-9][0-9][0-9][0-9]/)
puts latitude


#(0..links4.length-1).each do |i|
=begin
postalcode = []
(0..10).each do |i|
  space_location = links4[i].index(' ')
  #puts ("Station #{i} space location: #{space_location}")
  station_name = links4[i][space_location,links4[i].length]
  puts ("Station #{i} name: #{station_name}")
  station_url = base_url + links4[i][1,space_location-1]
  puts ("Station #{i} URL: #{station_url}")
  #station_html = ScraperWiki.scrape(station_url)
  station_html = Nokogiri::HTML(open(station_url))
  #puts ("Station #{i} HTML: #{station_html}")
  postalcode = station_html.search("td div div div div div").to_s.scan(/[A-Z]\d[A-Z] \d[A-Z]\d/)
  puts ("Station #{i} postal code: #{postalcode}")
  latitude = station_html.search("td div div div iframe").to_s.scan(/[4-5][0-9]\.[0-9][0-9][0-9][0-9]/)
  puts ("Station #{i} latitude: #{latitude}")
  longitude = station_html.search("td div div div iframe").to_s.scan(/[6-9][0-9]\.[0-9][0-9][0-9][0-9]/)
  if (!longitude.to_s.empty?)
    longitude = "-" + longitude.to_s
  end
  puts ("Station #{i} longitude: #{longitude}")
  #ScraperWiki.save(['Stop', 'Postal code'],
  #  {'Stop' => links[i][35,99], 'Postal code' => postalcode })
  ScraperWiki.save(['Station', 'PostalCode', 'Latitude', 'Longitude'], {'Station' => station_name, 'PostalCode' => postalcode, 'Latitude' => latitude, 'Longitude' => longitude })
end
=end

#print all elements of the array
#(0..links.length).each do |i|
#  puts ("links#{i}: #{links[i]}")
#end

