# Blank Ruby

require 'rfgraph'

req = RFGraph::Request.new      
  
res= req.get_object("PBSHawaii")  # https://graph.facebook.com/USERID

puts res["website"]
puts res["name"] 
puts res["about"]
puts res["description"]
puts res["location"]
puts res["phone"]
puts res["category"]
puts res["link"]
puts res["source"]

res2= req.get_object("SouthMauiSustainability")  # https://graph.facebook.com/USERID

puts res2["website"]
puts res2["name"] 
puts res2["about"]
puts res2["description"]
puts res2["location"]
puts res2["phone"]
puts res2["category"]
puts res2["link"]
puts res2["source"]





print "Creating a text file with the write() method."
text_file = open("write_it.txt", "w")
text_file.write("Line 1\n")
text_file.write("This is line 2\n")
text_file.write("That makes this line 3\n")
text_file.close()

