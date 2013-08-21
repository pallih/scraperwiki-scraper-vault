require 'json'

data = JSON(ScraperWiki::scrape("http://nectar.northampton.ac.uk/cgi/search/archive/advanced/export_northampton_JSON.js?screen=Search&dataset=archive&_action_export=1&output=JSON&exp=0%7C1%7C-date%2Fcreators_name%2Ftitle%7Carchive%7C-%7Ccreators_name%3Acreators_name%3AALL%3AEQ%3Aollerton%7Ctype%3Atype%3AANY%3AEQ%3Aarticle%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive&n=&cache=3580861").force_encoding("UTF-8"))

d=data[1]
puts d
d["creators"].each do |c|
  puts "#{c['name']['family']}, #{c['name']['given']}"
end



