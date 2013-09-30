require "mechanize"

# we need some methods to clean this up so make it a class

class InspectionScraper

  BASE_URL         = "http://eats.washoecounty.us/"
  FACILITY_COLS    = ["link", "name", "score", "facility_type", "address", "inspection_date"]
  RESULTS_TABLE_ID = "table#ctl00_ContentPlaceHolder1_grdHealth"

  def initialize
    @m = Mechanize.new

    ## agent setup
    @m.agent.keep_alive = false
    @m.agent.read_timeout = 60
    @m.agent.retry_change_requests = true
    # @m.agent.http.debug_output = $stdout
    @m.user_agent_alias = 'Mac Safari'
  end

  def scrape
    process_facilities
  end

  private

  # we may need these later
  # form.add_field!("__EVENTTARGET",'ctl00$ContentPlaceHolder1$grdHealth')
  # form.add_field!("__EVENTARGUMENT", 'Page$2')

  def process_facilities(page=nil, page_number=nil)   

    page ||= @m.get(BASE_URL)

    form = page.form("aspnetForm")
    form["ctl00$ContentPlaceHolder1$btnSearch"] = "Search" unless page_number
    form["__EVENTTARGET"] = "ctl00$ContentPlaceHolder1$grdHealth"
    form["__EVENTARGUMENT"] = "#{page_number}"

    # filter for testing
    form["ctl00$ContentPlaceHolder1$txtCity"] = "RENO"
    #form["ctl00$ContentPlaceHolder1$txtFacilityType"] = "Snackbar"

    # return form results
    new_page = form.submit
    results = new_page.search(RESULTS_TABLE_ID)

    # array for rows
    rows = []

    results.xpath('tr').each do |tr|
      next if tr[:align] == "center"
    
      # hash per row of data
      row = {}
    
      # get data from cells
      tr.xpath('td').each_with_index do |td, i|
        row[FACILITY_COLS[i].to_sym] = if i == 0
          # get the link
          td.at_css("a")[:href].to_s.strip
        else
          td.text.to_s.strip
        end
      end
    
      # create a unique 'id'  
      row[:id] = row[:name].to_s.downcase.gsub(/\s/, "_")
    
      # debug row
      puts row.inspect
      
      # add the row
      rows << row
    end

    # save facilities
    ScraperWiki.save_sqlite(unique_keys=[:id], data=rows, table_name="facilities")
    
    if next_page = results.search('//td/table/tr/td[span]/following-sibling::td[1]/a[@href]')
      match = next_page.attribute("href").to_s.match(/Page\$(\d+)/)
      next_page_number = match ? match[0] : nil
      return if next_page_number.empty? 

      # the website hates us!
      sleep(3)
      process_facilities(new_page, next_page_number)
    end

  end

end # InspectionScraper

puts ">> run scraper"
InspectionScraper.new.scrape
require "mechanize"

# we need some methods to clean this up so make it a class

class InspectionScraper

  BASE_URL         = "http://eats.washoecounty.us/"
  FACILITY_COLS    = ["link", "name", "score", "facility_type", "address", "inspection_date"]
  RESULTS_TABLE_ID = "table#ctl00_ContentPlaceHolder1_grdHealth"

  def initialize
    @m = Mechanize.new

    ## agent setup
    @m.agent.keep_alive = false
    @m.agent.read_timeout = 60
    @m.agent.retry_change_requests = true
    # @m.agent.http.debug_output = $stdout
    @m.user_agent_alias = 'Mac Safari'
  end

  def scrape
    process_facilities
  end

  private

  # we may need these later
  # form.add_field!("__EVENTTARGET",'ctl00$ContentPlaceHolder1$grdHealth')
  # form.add_field!("__EVENTARGUMENT", 'Page$2')

  def process_facilities(page=nil, page_number=nil)   

    page ||= @m.get(BASE_URL)

    form = page.form("aspnetForm")
    form["ctl00$ContentPlaceHolder1$btnSearch"] = "Search" unless page_number
    form["__EVENTTARGET"] = "ctl00$ContentPlaceHolder1$grdHealth"
    form["__EVENTARGUMENT"] = "#{page_number}"

    # filter for testing
    form["ctl00$ContentPlaceHolder1$txtCity"] = "RENO"
    #form["ctl00$ContentPlaceHolder1$txtFacilityType"] = "Snackbar"

    # return form results
    new_page = form.submit
    results = new_page.search(RESULTS_TABLE_ID)

    # array for rows
    rows = []

    results.xpath('tr').each do |tr|
      next if tr[:align] == "center"
    
      # hash per row of data
      row = {}
    
      # get data from cells
      tr.xpath('td').each_with_index do |td, i|
        row[FACILITY_COLS[i].to_sym] = if i == 0
          # get the link
          td.at_css("a")[:href].to_s.strip
        else
          td.text.to_s.strip
        end
      end
    
      # create a unique 'id'  
      row[:id] = row[:name].to_s.downcase.gsub(/\s/, "_")
    
      # debug row
      puts row.inspect
      
      # add the row
      rows << row
    end

    # save facilities
    ScraperWiki.save_sqlite(unique_keys=[:id], data=rows, table_name="facilities")
    
    if next_page = results.search('//td/table/tr/td[span]/following-sibling::td[1]/a[@href]')
      match = next_page.attribute("href").to_s.match(/Page\$(\d+)/)
      next_page_number = match ? match[0] : nil
      return if next_page_number.empty? 

      # the website hates us!
      sleep(3)
      process_facilities(new_page, next_page_number)
    end

  end

end # InspectionScraper

puts ">> run scraper"
InspectionScraper.new.scrape
