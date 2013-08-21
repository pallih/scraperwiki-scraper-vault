# Blank Ruby
# A simple example of CSV parsing, using Ruby.


require 'csv'
data = ScraperWiki.scrape("http://dl.dropbox.com/u/99174936/newtest.csv")           
csv = CSV.new(data)



require 'rfgraph'
req = RFGraph::Request.new      
  i="DailyMonitor"
  j="aljazeera"
res= req.get_object(i)

# https://graph.facebook.com/logicus


puts res["name"]
puts res["likes"]
puts res["talking_about_count"]

res= req.get_object(j)
puts res["name"]
puts res["likes"]
puts res["talking_about_count"]







#puts res["website"]
#puts res["name"]
#puts res["likes"]
#puts res["talking_about_count"]
#puts res["website"]
#puts res["likes"]
#puts res["talking_about_count"]

end





