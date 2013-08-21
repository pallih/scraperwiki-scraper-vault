require 'mechanize'
require 'date'
require 'logger'

base_url = "https://online.unley.sa.gov.au/ePathway/Production/Web/GeneralEnquiry/"
url = "#{base_url}enquirylists.aspx"

agent = Mechanize.new do |a|
a.keep_alive = false # to avoid a "Net::HTTP::Persistent::Error:too many connection resets" condition
                     # https://github.com/tenderlove/mechanize/issues/123#issuecomment-6432074

#a.log = Logger.new $stderr
#a.agent.http.debug_output = $stderr
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

first_page = agent.get url
p first_page.title.strip
first_page_form = first_page.forms.first
first_page_form.radiobuttons[1].click
search_page = first_page_form.click_button

p search_page.title.strip
search_form = search_page.forms.first
# get the button you want from the form
button = search_form.button_with(:value => "Search")
# submit the form using that button
summary_page = agent.submit(search_form, button)
p summary_page.title.strip

das_data = []
while summary_page
  table = summary_page.root.at_css('.ContentPanel')
  #p table
  headers = table.css('th').collect { |th| th.inner_text.strip } 
  p headers

  das_data = das_data + table.css('.ContentPanel, .AlternateContentPanel').collect do |tr| 
    tr.css('td').collect { |td| td.inner_text.strip }
  end

  next_page_img = summary_page.root.at_xpath("//a/img[contains(@src, 'nextPage')]")
  summary_page = nil
  if next_page_img
    p "Found another page"
    summary_page = agent.get "#{base_url}#{next_page_img.parent['href']}"
  end
end

comment_url = 'mailto:pobox1@unley.sa.gov.au'

das = das_data.collect do |da_item|
  page_info = {}
  page_info['council_reference'] = da_item[headers.index('Number')]
  # There is a direct link but you need a session to access it :(
  page_info['info_url'] = url
  page_info['description'] = da_item[headers.index('Description')]
  page_info['date_received'] = Date.strptime(da_item[headers.index('Date Lodged')], '%d/%m/%Y').to_s
  page_info['address'] = da_item[headers.index('Location')]
  page_info['date_scraped'] = Date.today.to_s
  page_info['comment_url'] = comment_url
  
  page_info
end

das.each do |record|
    ScraperWiki.save_sqlite(['council_reference'], record)
end

