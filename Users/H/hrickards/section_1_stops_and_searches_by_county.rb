require 'spreadsheet'           
require 'open-uri'

# A list of the welsh forces we can ignore.
welsh_counties = ["Dyfed-Powys", "Gwent", "North Wales", "South Wales"]

# The URL containing the stop and search figures. It is not clear whether this spreadsheet will be updated, or whether
# we'll have to replace the URL.
url = "http://www.parliament.uk/deposits/depositedpapers/2010/DEP2010-2056.xls"

# Open the spreadsheet. All of the spreadsheet code based upon
# https://scraperwiki.com/docs/ruby/ruby_excel_guide/.
book = nil
open url do |f|
  book = Spreadsheet.open f
end

# Open the sheet containing section 1 stops and searches.
sheet = book.worksheet "Section 1 Stop and Search"

# For each row.
sheet.each_with_index do |row, rownumber|
  # Ignore the first 8 rows - they don't contain data.
  unless rownumber < 8
    # Get the force name and total number of stops and searches.
    force = row[2]
    total_stops_and_searches = row[15]

    # As long as both the force name and total stops and searches are not blank, and the
    # force name is not "England and Wales" (the totals row) or a welsh county...
    unless force == nil or force == "England and Wales" or welsh_counties.include? force or total_stops_and_searches == nil
      # Downcase, humanise any ampsersands,dash the force name and remove any "-police"s
      force = force.downcase.gsub("&", "and").gsub(" ", "-").gsub("-police", "")

      # Replace "london,-city-of" with city-of-london
      force = "city-of-london" if force == "london,-city-of"

      # Add the county name and the total number of stops and searches to the ScraperWiki DB.
      ScraperWiki.save_sqlite unique_keys = ['force'], data = {'force' => force, 'total_stops_and_searches' => total_stops_and_searches}
    end
  end
endrequire 'spreadsheet'           
require 'open-uri'

# A list of the welsh forces we can ignore.
welsh_counties = ["Dyfed-Powys", "Gwent", "North Wales", "South Wales"]

# The URL containing the stop and search figures. It is not clear whether this spreadsheet will be updated, or whether
# we'll have to replace the URL.
url = "http://www.parliament.uk/deposits/depositedpapers/2010/DEP2010-2056.xls"

# Open the spreadsheet. All of the spreadsheet code based upon
# https://scraperwiki.com/docs/ruby/ruby_excel_guide/.
book = nil
open url do |f|
  book = Spreadsheet.open f
end

# Open the sheet containing section 1 stops and searches.
sheet = book.worksheet "Section 1 Stop and Search"

# For each row.
sheet.each_with_index do |row, rownumber|
  # Ignore the first 8 rows - they don't contain data.
  unless rownumber < 8
    # Get the force name and total number of stops and searches.
    force = row[2]
    total_stops_and_searches = row[15]

    # As long as both the force name and total stops and searches are not blank, and the
    # force name is not "England and Wales" (the totals row) or a welsh county...
    unless force == nil or force == "England and Wales" or welsh_counties.include? force or total_stops_and_searches == nil
      # Downcase, humanise any ampsersands,dash the force name and remove any "-police"s
      force = force.downcase.gsub("&", "and").gsub(" ", "-").gsub("-police", "")

      # Replace "london,-city-of" with city-of-london
      force = "city-of-london" if force == "london,-city-of"

      # Add the county name and the total number of stops and searches to the ScraperWiki DB.
      ScraperWiki.save_sqlite unique_keys = ['force'], data = {'force' => force, 'total_stops_and_searches' => total_stops_and_searches}
    end
  end
end