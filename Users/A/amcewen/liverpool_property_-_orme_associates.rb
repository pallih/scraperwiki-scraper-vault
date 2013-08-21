# Blank Ruby
require "nokogiri"


# Function to try to map an address to a lat/lng using Geonames
# Takes an address string and return an array of [lat, lng] or nil if the address couldn't be mapped
def gb_address_to_latlng(address)
  encoded_address = CGI.escape(address)
  result = ScraperWiki.scrape("http://api.geonames.org/search?q=#{encoded_address}&country=gb&username=amcewen&maxRows=1")
  result_doc = Nokogiri::HTML(result)
  unless result_doc.css("geoname").empty? 
    return [result_doc.css("geoname lat").inner_text, result_doc.css("geoname lng").inner_text]
  else
    # We seem to get addresses like "Lowestoft, Suffolk, South East" and Geonames doesn't like
    # the "South East" part, so try removing the last clause
    addr_clauses = address.split(',')
    if addr_clauses.size > 1
      addr_clauses.delete_at(addr_clauses.size-1)
      return gb_address_to_latlng(addr_clauses.join(", "))
    else
      return nil
    end
  end
end

def add_property(url)
  #property_
end

index_page = ScraperWiki.scrape("http://www.orme-associates.co.uk/industrial.php")
index_doc = Nokogiri::HTML(index_page, nil, 'utf-8')

# Iterate through all of the properties
index_doc.css("a.style1").each do |link|
  if link.inner_text == "Sales Particulars"
    # Check to see if we've already seen these details
    # Add this property to the database
    add_property(link['href'])
  else
    puts "Skipping link "+link.inner_text
  end
end

