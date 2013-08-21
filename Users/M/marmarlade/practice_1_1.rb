# Blank Ruby

require 'open-uri' #library that goes out to the web and opens a URL and sucks whatever's there in.
require 'json' #json is javascript object notation - common way for storing data for a lot of web apps. turns it into something more structured than just javascript.

site = "http://submarinecablemap.com/javascripts/cables/all.json"
data = JSON.parse(open(site).read) #parsing the information that is coming back in - json/JSON caps sensitive

data.each do |cable|
puts cable['name'] + ", " + cable['rfs']

end

#elements = ["one","two","three"]

#counter = 0
#while counter < elements.length
#  puts elements[counter]
#  counter = counter + 1
#end

#elements.each {|element|puts element}
