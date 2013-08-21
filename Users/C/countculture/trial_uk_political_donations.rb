require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

starting_url = 'https://pefonline.electoralcommission.org.uk/search/searchintro.aspx'

# starting_url = BASE_URL + 'pvi/CompanySearch.aspx'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
  browser.verify_mode = OpenSSL::SSL::VERIFY_NONE
  browser.gzip_enabled = false
  browser.log = Logger.new(STDERR)
}
# get first page to pick up cookies etc
@page = @br.get(starting_url)
@page.form_with(:name => 'aspnetForm') do |f|
  f['ctl00$ctl04$ctl01'] = 'Advanced donations search'
  @page = f.submit
end

@page = @br.get('https://pefonline.electoralcommission.org.uk/Search/CommonReturnsSearch.aspx?type=advDonationSearch')

f = @page.form_with(:name => 'aspnetForm')
f['ctl00$ContentPlaceHolder1$searchControl1$cmbCriteriaType'] = 'Company, Limited Liability Partnership'
button = f.button_with(:value=>"Export results to CSV file")
@page = @br.submit(f, button) #THIS IS CURRENTLY RAISING EOFERROR

