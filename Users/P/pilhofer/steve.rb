# Blank Ruby

require 'open-uri'
require 'json'
require 'mechanize'

site = "http://submarinecablemap.com/javascripts/cables/all.json"
data = JSON.parse(open(site).read )

data.each do |cable|

puts cable['name'] + ", " + cable['rfs']

end