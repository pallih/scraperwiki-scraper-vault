require 'nokogiri'           

html=ScraperWiki.scrape('http://www.bom.gov.au/products/IDQ60901/IDQ60901.94580.shtml')
doc = Nokogiri::HTML(html)
for table in doc.search("table")
  #Ignore the header because it's weird.
  for tr in table.xpath("tr[td]")
    keys = tr.xpath('td/attribute::headers')
    values = tr.xpath('td/text()')
    puts keys.to_json
    puts values.to_json
    #data=Hash[keys.zip(values)]
    #puts data.to_json
  end
end