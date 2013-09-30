# Blank Ruby

require 'rfgraph'

req = RFGraph::Request.new      
  
res= req.get_object("SandiKrakowskiBiz")  # https://graph.facebook.com/116771361715257

puts res["website"]
puts res["name"] 
puts res["likes"]
puts res["timelineLikesMetricTitle"]









