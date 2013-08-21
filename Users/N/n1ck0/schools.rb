# direct.gov Schools Finder
# Objective: create index of schools within n miles radius of a postcode.
# To add: deduping of search results
  
require 'nokogiri'
require 'open-uri'

# Function to initialize Nokogiri object
def scrape(uri)
  return Nokogiri::HTML(open(uri), nil, "UTF-8")
end

# Create table.
table_name = 'schools 20mi from Liverpool' # Or whatever
#ScraperWiki::sqliteexecute("drop table if exists `#{table_name}`")
ScraperWiki::sqliteexecute("create table `#{table_name}` (name string, address string, `head teacher` string, telephone string, `school website` string, `type of school` string, `age range` string, gender string, `number of pupils` int, `funding type` string, `religious affiliation` string, features string, specialisms string, lea string, `local authority website` string, lat float, lon float)") 

domain = "http://schoolsfinder.direct.gov.uk"
path = "/search-results/"
parameters = {
              "searchstringrefine" => "L1 4DQ".gsub(/\s/,"+"), # Enter your postcode
              "distanceValue" => 20 # Enter the search radius in miles
              
              # Schools Finder seems to not return more than 500 results per query. Annoyingly, some of
              # the results are duplicates. Multiple queries across small, overlapping zones would probably
              # be more complete than a single, large radius query (altho incidence of duplicate results 
              # would increase); prob 5mi or less, def less in London
                                      
              # There are other options for refining search but I'm leaving them out for now
             }

query_string = "?" + parameters.to_a.map{ |a| a.join("=") }.join("&") # Join parameters, prefix
uri = domain + path + query_string
html = scrape(uri)
x = "//ul[@class='paging']/li/a[contains(text(), 'Next')]" # Xpath for 'next' button, key to pagination
pages = true 
while pages 
  # Each page contains 10 results by default
  results = html.css("div[class='info-panel wide result']")
  results.each do |result|
    heading = result.css("h3 a").last # There are always 2 <a> tags that head each result. First is Javascript, we want the last
    profile_uri = heading.css("@href").to_s.gsub(/\s/,"+") # Replace whitespace, prevents 'Bad URI' errors
    begin
      profile = scrape(profile_uri)  
    rescue # Exception handling: move to next in loop if scrape request comes back 404. 
      puts "#{heading.text.strip}: failed" # It's universities that come back 404. Why they're in Schools finder results I dunno 
      next
    end
    # Parse the profile html
    school = {} # (...we'll stash our data in this hash)
    
    # First the name...
    school["name"] = profile.title.split(":").first.split("-").last    
    
    # ...Then the main details
    overview = profile.css("div.tabbody").first
    # Convert each tab to a string, split it...
    overview = overview.to_s.split('<span class="clearLeft"></span>')
    # ...then create new Nokogiri objs to access the split up elements
    overview.each do |item|
      # Each item follows the pattern <span>Key</span> Value ie. <span>Head teacher:</span> Mr J. Smith
      item = Nokogiri::HTML(item)
      item_title = item.css("span.itemDetailTitle")
      key = item_title.text.strip[0..-2].downcase # Remove trailing colon, make lower case 
      item_title.remove # Once we have our key, remove it from the 'item' HTML
      if key == "local authority website"
        value = item.css("a/@href").to_s
        school["lea"] = item.text
      else # Except for the key above, we just want the remaining text
        value = item.text
      end
      school[key] = value unless key.empty? 
    end

    # Clean hash values of unwanted chars
    school.each_pair { |key, value| school[key] = value.strip.gsub(/\s{2,}/," ") }

    # Now add the location
    loc = profile.css("input#mapStartPoint/@value").to_s.split(",")
    school["lat"], school["lon"] = loc.first, loc.last
     
    # Build SQL statement. I don't know if this is the right or wrong way of going about this...
    columns = school.keys.map{ |item| "`#{item}`" }.join(", ") # Hash keys correspond to the columns we want to INSERT to
    values = school.values
    no_of_values = values.length
    bindings = (['?'] * no_of_values).join(',') # Create bindings depending on how many columns we are INSERTing to

    # Execute SQL statement. Scraperwiki takes care of escaping our values!
    ScraperWiki::sqliteexecute("insert into `#{table_name}` (#{columns}) values (#{bindings})", values)
  end

  # Paginate
  next_link = html.xpath(x)
  if next_link.empty? 
    pages = !pages # No 'next' link will cause the loop to stop
  else
    query_string = next_link.first.css("@href").to_s
    uri = domain + path + query_string
    html = scrape(uri)
  end
end
ScraperWiki::commit()