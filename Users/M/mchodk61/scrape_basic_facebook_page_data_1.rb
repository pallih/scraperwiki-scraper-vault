# Blank Ruby

require 'rfgraph'

req = RFGraph::Request.new      
  
# https://graph.facebook.com/logicus

res= req.get_object("archiduchesse") 
puts res["name"]
puts res["likes"]
puts res["category"]



res= req.get_object("DailyMonitor") 
puts res["name"]
puts res["likes"]
puts res["talking_about_count"]
