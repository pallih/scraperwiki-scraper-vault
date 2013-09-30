# A simple example of CSV parsing, using Ruby.
require 'csv'
require 'rfgraph'

data = ScraperWiki.scrape("http://dl.dropbox.com/u/99174936/csv%20test2.csv")           

csv = CSV.new(data)


#csv.each do |row|
#  puts format("%s", row[1++],)

#puts data
p data


req = RFGraph::Request.new  
#array = ["http://www.facebook.com/hindustantimes"]
#res= req.get_object(i)
#array.each { |"name"|
#puts res["name"]}
# A simple example of CSV parsing, using Ruby.
require 'csv'
require 'rfgraph'

data = ScraperWiki.scrape("http://dl.dropbox.com/u/99174936/csv%20test2.csv")           

csv = CSV.new(data)


#csv.each do |row|
#  puts format("%s", row[1++],)

#puts data
p data


req = RFGraph::Request.new  
#array = ["http://www.facebook.com/hindustantimes"]
#res= req.get_object(i)
#array.each { |"name"|
#puts res["name"]}
