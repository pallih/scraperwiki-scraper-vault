ScraperWiki::httpresponseheader("Content-Type", "application/xml")
ScraperWiki::attach('uol_pc_availabilty') 
data = ScraperWiki::select('* FROM uol_pc_availabilty.swdata')
now  = Time.now.strftime("%Y-%m-%dT%H:%M:%S.%L")

xml =  "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
xml << "<pc_labs>\n"
xml << "  <updated>#{now}</updated>\n"

data.each do |lab|
  xml << "  <lab name=\"#{lab['name']}\">\n"
  xml << "    <location lat=\"#{lab['lat']}\" lng=\"#{lab['lng']}\"/>\n"
  xml << "    <computers total=\"xxx\" available=\"#{lab['num_pcs']}\"/>"
  xml << "  </lab>\n"
end

xml << "</pc_labs>"

puts xmlScraperWiki::httpresponseheader("Content-Type", "application/xml")
ScraperWiki::attach('uol_pc_availabilty') 
data = ScraperWiki::select('* FROM uol_pc_availabilty.swdata')
now  = Time.now.strftime("%Y-%m-%dT%H:%M:%S.%L")

xml =  "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
xml << "<pc_labs>\n"
xml << "  <updated>#{now}</updated>\n"

data.each do |lab|
  xml << "  <lab name=\"#{lab['name']}\">\n"
  xml << "    <location lat=\"#{lab['lat']}\" lng=\"#{lab['lng']}\"/>\n"
  xml << "    <computers total=\"xxx\" available=\"#{lab['num_pcs']}\"/>"
  xml << "  </lab>\n"
end

xml << "</pc_labs>"

puts xml