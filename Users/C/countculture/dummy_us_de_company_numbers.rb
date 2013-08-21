require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'https://delecorp.delaware.gov/tin/controller'

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body)
  data_table = Nokogiri::HTML(page_body).css('table#WFDGRDCompanies tr.resultsGridBody').collect do |row|
    record = {}
    record['CompanyNumber']   = row.css('td')[0].inner_text.strip
    record['CompanyName']     = row.css('td')[1].inner_text.strip
    record['date_scraped']    = Time.now
    begin
      ScraperWiki.save(["CompanyNumber"], record)
    rescue Exception=>e
      puts "Exception (#{e.inspecy}) raised saving company record:#{record.inspect}"
    end
  end
end
        
# Scrape page, look for 'next' link: if found, submit the page form
def extract_data_and_get_next_page
  scrape_table(@page.body)
  link = @page.at('table#WFDGRDCompanies tr.form span~a') # get the link after the current page (which is the only one in a span)
    
  if link
    @page.form_with(:name => 'eForm') do |f|
      #f['__EVENTTARGET'] = link[:href].scan(/WFDGRDCompanies[^']+/).to_s.gsub('$',':')
      #f['__EVENTARGUMENT'] = ''
      @page = f.submit
    end
    extract_data_and_get_next_page
  end
rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
  puts "Exception raised while getting data: #{e.inspect}"
end

def get_first_page_of_search(term)
  @page.form_with(:name => 'eForm') do |f|
    f['WFTBCompanyName'] = term
    @page = f.submit
  end
end


# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

#starting_url = BASE_URL + 'pvi/CompanySearch.aspx'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}
# get first page to pick up cookies etc
@page = @br.get(BASE_URL)

#@br = 
    @page.form_with(:name => 'GINS') do |f|
      f['frmEntityName'] = 'AAAAA'
      #f['__EVENTARGUMENT'] = ''
      @page = f.submit
      puts @page
    end
exit

initial_first_letter = ScraperWiki.get_var('first_letter', 'a')
initial_last_letter = ScraperWiki.get_var('last_letter', 'a')
initial_first_letter, initial_last_letter = 'a','a' if (initial_first_letter == 'z') && (initial_last_letter == 'z')
(initial_first_letter..'z').each do |first_letter|
  (initial_last_letter..'z').each do |last_letter|
    begin
      get_first_page_of_search(first_letter + last_letter)
      extract_data_and_get_next_page
      puts "finished getting details for '#{first_letter + last_letter}'"
    rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
      puts "Exception raised while getting first page of search: #{e.inspect}"
    end
    ScraperWiki.save_var('last_letter', last_letter)
    initial_last_letter = 'a' if initial_last_letter == 'z'
  end
  ScraperWiki.save_var('first_letter', first_letter)
end
