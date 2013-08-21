# Scraper for properties in L8 on Entwistle Green's website
require 'mechanize'
require 'json'

parent_search_url = 'http://www.entwistlegreen.co.uk/buy/search/l8/within-1-miles/order-pricedescending/'
SEARCH_POST_DATA = '{"SearchString":"L8","AskingPriceMin":0,"AskingPriceMax":99999999,"BedroomsMin":0,"BedroomsMax":99,"ReceptionsMin":0,"ReceptionsMax":99,"BathroomsMin":0,"BathroomsMax":99,"OrderBy":"Default","CurrentPage":"1","ResultsPageSize":10,"Latitude":"0.00","Longitude":"0.00","Radius":1,"TenureTypeID":-1,"PropertyTypeID":-1,"PromotionID":0}'
SEARCH_POST_URL = 'http://www.entwistlegreen.co.uk/webservices/forsalesearch.asmx/GetPropertyListings'


def search_page(page_num)
  # Update the page number
  post_data = SEARCH_POST_DATA.gsub(/"CurrentPage"\:"\d+"/, '"CurrentPage":"'+page_num.to_s+'"')

  # Get the search results
  results = @agent.post(SEARCH_POST_URL, post_data, 'Content-Type' => 'application/json; charset=utf-8')

  if results.code == "200"
    # We were successful, record these details
    parsed_results = JSON.parse(results.body)

    puts "Page #{page_num}: "+parsed_results['d']['ContentContainer']['PropertyListings'].size.to_s+" results"
    parsed_results['d']['ContentContainer']['PropertyListings'].each do |property|
      #puts property.inspect
      # We don't care about the promotions field (as it's a tricky to store array)
      property.delete('Promotions')
      # See if we've already seen this property
      old_property = ScraperWiki.sqliteexecute("select * from swdata where InstructionID = "+property["InstructionID"].to_s)
      #puts old_property.inspect
      if old_property['data'].empty? 
puts "first seen"
        property['first_seen'] = Date.today.to_s
        property['first_price'] = property['Price']
      end
      property['last_seen'] = Date.today.to_s
      # Save it to the database
      ScraperWiki.save_sqlite(["InstructionID"], property)
    end

    if parsed_results['d']['ContentContainer']['PropertyListings'].empty? 
      # We've reached the end of the results
      false
    else
      true
    end
  else
    # It failed for some reason
    puts "Got response code #{results.code}"
    false
  end
end


@agent = Mechanize.new

# Get the search page first so we get a cookie
@agent.get(parent_search_url)

page = 1
while search_page(page) do
  #puts page.to_s
  page = page + 1
end


