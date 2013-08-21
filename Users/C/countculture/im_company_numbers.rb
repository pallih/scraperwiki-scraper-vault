require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

# ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
# exit

ALPHA_PLUS_DIGITS = ("A".."Z").to_a + ("0".."9").to_a
POSSIBLE_PREFIXES = ALPHA_PLUS_DIGITS.map{|l| ALPHA_PLUS_DIGITS.map{|l2| l+l2}}.flatten

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://portal.gov.im/'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  data_table = Nokogiri::HTML(page_body).css('table#WFDGRDCompanies tr.resultsGridBody').collect do |row|
    record = {}
    record['CompanyNumber']   = row.css('td')[0].inner_text.strip
    record['CompanyName']     = row.css('td')[1].inner_text.strip
    record['Status']          = row.css('td')[2].inner_text.strip
    record['EntityType']      = row.css('td')[3].inner_text.strip
    record['NameType']        = row.css('td')[4].inner_text.strip
    record['date_scraped']    = Time.now
    next if ['NameType'] == 'PREVIOUS' #these have the same company numbers as 'CURRENT' ones, and so would over-write them. Previous name details are avail on the company page, so we can discard this info
    begin
      ScraperWiki.save(["CompanyNumber"], record)
    rescue Exception=>e
      puts "Exception (#{e.inspect}) raised saving company record:#{record.inspect}"
    end
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def extract_data_and_get_next_page
  scrape_table(@page.body)
  link = @page.at('table#WFDGRDCompanies tr.form span~a') # get the link after the current page (which is the only one in a span)
  if link && (event_target = link[:href].scan(/WFDGRDCompanies[^']+/).first.gsub('$',':')) 
    form = @page.form_with(:name => 'eForm')
    @page = submit_form_with_event_target(form, event_target)
    extract_data_and_get_next_page
  end
#rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
#  puts "Exception raised while getting data: #{e.inspect}"
end

def get_first_page_of_search(term)
  @page.form_with(:name => 'eForm') do |f|
    f['WFTBCompanyName'] = term
    @page = f.submit
  end
end

def submit_form_with_event_target(form, et)  
  form['__EVENTTARGET'] = et
  form['__EVENTARGUMENT'] = ''
  res = form.submit
  @sleep_time = 0 # reset
  res
rescue Timeout::Error
  @sleep_time +=60
  raise "Too many failed Timeouts" if @sleep_time > 300
  puts "Timeout while getting data. Sleeping for #{@sleep_time} seconds before trying again"
  sleep @sleep_time
  submit_form_with_event_target(form, et) 
end


# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = BASE_URL + 'pvi/CompanySearch.aspx'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}
# get first page to pick up cookies etc
@page = @br.get(starting_url)

start_position = POSSIBLE_PREFIXES.index ScraperWiki.get_var('letters', "AA")

POSSIBLE_PREFIXES[start_position..-1].each do |letters|
  ScraperWiki.save_var('letters', letters) # save letters in case scraper gets killed
  puts "About to get details for '#{letters}'"
  get_first_page_of_search(letters)
  extract_data_and_get_next_page
  puts "finished getting details for '#{letters}'"
end
ScraperWiki.save_var('letters','AA') # if we've got this far we need to start at the beginning next time
