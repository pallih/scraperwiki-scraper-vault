###############################################################################
# CA Interpreters
###############################################################################

require 'nokogiri'
require 'open-uri'

# retrieve a page
BASE_URL  = 'http://www.yellowpages.com'
FIRST_EXT = '/ca/interpreters?g=CA'

# define the order our columns are displayed in the datastore
mdc = SW_MetadataClient.new
mdc.save('data_columns', ['Business', 'Address', 'Hours', 'Categories', 'Accreditations', 'In Business Since', 'General Info', 'Products/Services', 'Extra Phones/Fax', 'Web Links', 'City', 'State', 'Zipcode', 'Phone']) 

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  page.css('.listing_content').collect do |x|
    record = {}
    record['Business']  = x.css('.business-name a').text
    record['Address']   = x.css('.street-address').text.sub(/,[\s]*/, '') || "not listed"
    record['City']      = x.css('.locality').text || "not listed"
    record['State']     = x.css('.region').text || "not listed"
    record['Zipcode']   = x.css('.postal-code').text || "not listed"
    record['Phone']     = x.css('.business-phone').text || "not listed"

    ## collect secondary info
    url = x.at_css('.business-name a').attribute("href")
    page2 = Nokogiri::HTML(open(url))
    ext_record = scrape_page2(page2)
    
    record.merge!(ext_record)
    ScraperWiki.save(["Business"], record)
  end
end

# scrape_table function: gets passed an individual page to scrape
def scrape_page2(page2)
  
  record = {}

  record['Hours'] = 'not listed'
  record['Categories'] = 'not listed'
  record['In Business Since'] = 'not listed'
  record['General Info'] = 'not listed'
  record['Accreditations'] = 'not listed'
  record['Products/Services'] = 'not listed'
  record['Extra Phones/Fax'] = 'not listed'
  record['Web Links'] = 'not listed'

  ## init last, current
  last    = "X"
  current = "X"

  page2.xpath('//dt | //dt/following-sibling::*[1][self::dd]').each do |node|
    current = node.text

    key = case last
      when "Hours" then "Hours"
      when "Categories" then "Categories"
      when "In Business Since" then "In Business Since"
      when "General Info" then "General Info"
      when "Products/Services" then "Products/Services"
      when "Extra Phones/Fax" then "Extra Phones/Fax"
      when "Web Links:" then "Web Links"
      else nil
    end

    unless key.nil? 
      record[key] = current
      ## puts "caught: #{last} -> #{current}"
    end

    last    = node.text

  end
  
  return record
end


#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))

    ## debugging note to the console
    puts 'scraping: '+url

    scrape_table(page)
    next_link = page.at_css('li.next')
    if next_link
      next_url = BASE_URL + next_link.at_css('a').attribute("href")
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL+FIRST_EXT
scrape_and_look_for_next_link(starting_url)
###############################################################################
# CA Interpreters
###############################################################################

require 'nokogiri'
require 'open-uri'

# retrieve a page
BASE_URL  = 'http://www.yellowpages.com'
FIRST_EXT = '/ca/interpreters?g=CA'

# define the order our columns are displayed in the datastore
mdc = SW_MetadataClient.new
mdc.save('data_columns', ['Business', 'Address', 'Hours', 'Categories', 'Accreditations', 'In Business Since', 'General Info', 'Products/Services', 'Extra Phones/Fax', 'Web Links', 'City', 'State', 'Zipcode', 'Phone']) 

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  page.css('.listing_content').collect do |x|
    record = {}
    record['Business']  = x.css('.business-name a').text
    record['Address']   = x.css('.street-address').text.sub(/,[\s]*/, '') || "not listed"
    record['City']      = x.css('.locality').text || "not listed"
    record['State']     = x.css('.region').text || "not listed"
    record['Zipcode']   = x.css('.postal-code').text || "not listed"
    record['Phone']     = x.css('.business-phone').text || "not listed"

    ## collect secondary info
    url = x.at_css('.business-name a').attribute("href")
    page2 = Nokogiri::HTML(open(url))
    ext_record = scrape_page2(page2)
    
    record.merge!(ext_record)
    ScraperWiki.save(["Business"], record)
  end
end

# scrape_table function: gets passed an individual page to scrape
def scrape_page2(page2)
  
  record = {}

  record['Hours'] = 'not listed'
  record['Categories'] = 'not listed'
  record['In Business Since'] = 'not listed'
  record['General Info'] = 'not listed'
  record['Accreditations'] = 'not listed'
  record['Products/Services'] = 'not listed'
  record['Extra Phones/Fax'] = 'not listed'
  record['Web Links'] = 'not listed'

  ## init last, current
  last    = "X"
  current = "X"

  page2.xpath('//dt | //dt/following-sibling::*[1][self::dd]').each do |node|
    current = node.text

    key = case last
      when "Hours" then "Hours"
      when "Categories" then "Categories"
      when "In Business Since" then "In Business Since"
      when "General Info" then "General Info"
      when "Products/Services" then "Products/Services"
      when "Extra Phones/Fax" then "Extra Phones/Fax"
      when "Web Links:" then "Web Links"
      else nil
    end

    unless key.nil? 
      record[key] = current
      ## puts "caught: #{last} -> #{current}"
    end

    last    = node.text

  end
  
  return record
end


#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))

    ## debugging note to the console
    puts 'scraping: '+url

    scrape_table(page)
    next_link = page.at_css('li.next')
    if next_link
      next_url = BASE_URL + next_link.at_css('a').attribute("href")
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL+FIRST_EXT
scrape_and_look_for_next_link(starting_url)
