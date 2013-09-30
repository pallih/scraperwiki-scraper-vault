###############################################################################
# Scrapes restaurant, hotel and B&B inspection data
###############################################################################
require 'nokogiri'
require 'open-uri'

PROVIDER_URL     = 'http://www.healthspace.ca'
SERVICE_URL      = '/Clients/VDH/VBeach/VBeach_Website.nsf'
FACILITY_LIST    = '/Food-List-ByFirstLetterInName?OpenView&RestrictToCategory='
FACILITY_HISTORY = '/Food-FacilityHistory?OpenView&RestrictToCategory='

categories = ['1', '2', '3', '5', '7', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


# todo - make a schema.  Apparently save_metadata is deprecated
#ScraperWiki.save_metadata('data_columns', ['URL', 'Timestamp'])

#
def scrape_report(url)
  puts "REPORT"
end

# scrape function: gets passed an individual page to scrape
def scrape_facility(url)
  puts url
  fac_page = Nokogiri::HTML(open(url))
  puts fac_page.children()[1]
  fac_page.xpath('//tr[position() > 1]').each do |tr|
    i = 0
    report_url = ""
    tr.xpath('td').each do |td|
      # td0 = Inspection Type, td1 = Inspection Date, td2 = Violations
      if i == 0
        a = td.xpath('a')
        report_url = (a.count() != 0 && a[0].attribute('href') != nil) ? a[0].attribute('href') : ""
      end
      puts td.text()
      i+=1
    end
    scrape_report(PROVIDER_URL + report_url)
  end
end


# scrape_category function: scrapes the category page
# then calls the scrape_facility function
def scrape_category(category)
  url = PROVIDER_URL + SERVICE_URL + FACILITY_LIST + category
  #puts url
  cat_page = Nokogiri::HTML(open(url))
  #puts cat_page
  cat_page.xpath('//tr[position() > 1]').each do |tr|
    i = 0
    fac_history_url = ""
    tr.xpath('td').each do |td|
      # td0 = Name, td1 = optional smoking status (image), td2 = Address, td3 = Last Inspection Date
      if i == 0
        a = td.xpath('a')
        fac_history_url = (a.count() != 0 && a[0].attribute('href') != nil) ? a[0].attribute('href') : ""
      end
      if i == 1
        puts td.xpath('img').count() > 0 ? "smoking policy unknown" : "non-smoking"
      else
        puts td.text()
      end
      i+=1
    end
    scrape_facility(PROVIDER_URL + fac_history_url)
  end
end

# ---------------------------------------------------------------------------
# MAIN: Scrape each category
# ---------------------------------------------------------------------------
categories.each { |category| scrape_category(category) }###############################################################################
# Scrapes restaurant, hotel and B&B inspection data
###############################################################################
require 'nokogiri'
require 'open-uri'

PROVIDER_URL     = 'http://www.healthspace.ca'
SERVICE_URL      = '/Clients/VDH/VBeach/VBeach_Website.nsf'
FACILITY_LIST    = '/Food-List-ByFirstLetterInName?OpenView&RestrictToCategory='
FACILITY_HISTORY = '/Food-FacilityHistory?OpenView&RestrictToCategory='

categories = ['1', '2', '3', '5', '7', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


# todo - make a schema.  Apparently save_metadata is deprecated
#ScraperWiki.save_metadata('data_columns', ['URL', 'Timestamp'])

#
def scrape_report(url)
  puts "REPORT"
end

# scrape function: gets passed an individual page to scrape
def scrape_facility(url)
  puts url
  fac_page = Nokogiri::HTML(open(url))
  puts fac_page.children()[1]
  fac_page.xpath('//tr[position() > 1]').each do |tr|
    i = 0
    report_url = ""
    tr.xpath('td').each do |td|
      # td0 = Inspection Type, td1 = Inspection Date, td2 = Violations
      if i == 0
        a = td.xpath('a')
        report_url = (a.count() != 0 && a[0].attribute('href') != nil) ? a[0].attribute('href') : ""
      end
      puts td.text()
      i+=1
    end
    scrape_report(PROVIDER_URL + report_url)
  end
end


# scrape_category function: scrapes the category page
# then calls the scrape_facility function
def scrape_category(category)
  url = PROVIDER_URL + SERVICE_URL + FACILITY_LIST + category
  #puts url
  cat_page = Nokogiri::HTML(open(url))
  #puts cat_page
  cat_page.xpath('//tr[position() > 1]').each do |tr|
    i = 0
    fac_history_url = ""
    tr.xpath('td').each do |td|
      # td0 = Name, td1 = optional smoking status (image), td2 = Address, td3 = Last Inspection Date
      if i == 0
        a = td.xpath('a')
        fac_history_url = (a.count() != 0 && a[0].attribute('href') != nil) ? a[0].attribute('href') : ""
      end
      if i == 1
        puts td.xpath('img').count() > 0 ? "smoking policy unknown" : "non-smoking"
      else
        puts td.text()
      end
      i+=1
    end
    scrape_facility(PROVIDER_URL + fac_history_url)
  end
end

# ---------------------------------------------------------------------------
# MAIN: Scrape each category
# ---------------------------------------------------------------------------
categories.each { |category| scrape_category(category) }