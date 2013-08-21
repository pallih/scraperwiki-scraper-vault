###############################################################################
# Gather all mass times in ireland
###############################################################################
require 'nokogiri'
require 'open-uri'
require 'uri'

BASE_URL = 'http://www.catholicireland.net'

# define the order our columns are displayed in the datastore
ScraperWiki.save_var('data_columns', ['ID', 'County', 'Church', 'Times'])

# scrape_table function: gets passed an individual page to scrape
def scrape_timesbycounty(page)
  rows = Array.new
  data_table = page.css('table a').collect do |row|
    record = {}
    if row['href'].include? "churchbycounty"
      rows.push(row)
    end
  end

  return rows
end

def scrape_area(page)
  churches = Array.new
  page.css('table a').collect do |row|
    record = {}
    if row['href'].include? "churchinfo"
      churches.push(row)
    end
  end

  return churches
end

def scrape_masstimes(page)
  times = Array.new
  page.css('#content table tr td table tr').collect do |row|
    times.push(row.css('td').inner_text.strip)
  end
  return times
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    i = 0;
    page = Nokogiri::HTML(open(url))
    counties = scrape_timesbycounty(page)
    counties.collect do |county|    
      if county 
        county_url = BASE_URL + URI.escape(county['href'])
        areapage = Nokogiri::HTML(open(county_url))
        churches = scrape_area(areapage)
        churches.collect do |church|    
          if church 
            church_url = BASE_URL + URI.escape(church['href'])
            masstimes = Nokogiri::HTML(open(church_url))
            times = scrape_masstimes(masstimes)
            puts "------------------------------------------"
            puts "county = " +county.inner_text.strip
            puts "church = " +church.inner_text.strip
            puts "times = " +times.map { |str| "'" + str.to_s + "'" }.join(",")
            puts "------------------------------------------"  
            i+=1
            record = {}
            record['ID']    = i    
            record['County']    = county.inner_text.strip    
            record['Church']    = church.inner_text.strip    
            record['Times']    = times.map { |str| "'" + str.to_s + "'" }.join(",")    
            ScraperWiki.save(["ID"], record)
          end
        end
      end
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

starting_url = BASE_URL + '/mass-times'
scrape_and_look_for_next_link(starting_url)