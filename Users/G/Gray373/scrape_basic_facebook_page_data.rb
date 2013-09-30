# Blank Ruby

require 'rfgraph'

req = RFGraph::Request.new      
  
res= req.get_object("DailyMonitor")  # https://graph.facebook.com/logicus

req each do |res|
puts format(res["id"],res["name"],res["link"])




# Blank Ruby

require 'rfgraph'

req = RFGraph::Request.new      
  
res= req.get_object("DailyMonitor")  # https://graph.facebook.com/logicus

req each do |res|
puts format(res["id"],res["name"],res["link"])




