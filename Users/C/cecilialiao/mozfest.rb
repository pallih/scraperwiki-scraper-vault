# Blank Ruby

puts "hello world"
name = 'testing some "quotes" '

puts name

ArrayExample = ["Cecilia", 1234, "blahblahblah"]

puts ArrayExample[0] + " Liao"

HashExample = {"Name" => "Cecilia", "Age" => 27, "Title" => "analyst"}

# hash allows ordering by the column title, unlike array done by number of element

puts HashExample["Name"]

#www.ruby-doc.org

elements = ["strawberry" ,"banana", "cherry"]
#counter = 0

#while counter < elements.length
#puts elements[counter]
#counter = counter + 1

#end

elements.each {|element| puts element}

#.each is a ruby notation for loops
#same as
# elements.each do |elements|
# puts elements

#www.rubygems.org

require 'open-uri'
require 'json'

site = http://www.submarinecablemap.com/javascripts/cables/all.json
data = JSON.parse(open(site).read)


puts data.first['url']

#data.each do |cable|
#puts cable['name']

#end









