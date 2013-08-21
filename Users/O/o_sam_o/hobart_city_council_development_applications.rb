require 'nokogiri'
require 'open-uri'
require 'date'

url = "http://www.hobartcity.com.au/go/AdvertisedApps/output.html"
doc = Nokogiri::HTML(open(url))

table = doc.at_css('table')
puts table
puts table.css('th')
headers = table.css('th').collect { |th| th.inner_text.strip }
puts headers

das_data = table.css('tbody tr:not(.rowHidden)').collect do |tr|
  tr.css('td').collect { |td| td.inner_text.strip }
end

comment_url = 'mailto:hcc@hobartcity.com.au?Subject='

das = das_data.collect do |da_item|
  page_info = {}
  page_info['council_reference'] = da_item[headers.index('DA Number')]
  # No direct link :(
  page_info['info_url'] = 'http://www.hobartcity.com.au/advertisedapps'
  page_info['description'] = da_item[headers.index('Proposed Development')]
  page_info['date_received'] = Date.today.to_s
  page_info['address'] = "#{da_item[headers.index('Address')]}, TAS"
  page_info['on_notice_to'] = Date.strptime(da_item[headers.index('Representation Period Expiry Date')], '%d %B %Y').to_s
  page_info['date_scraped'] = Date.today.to_s
  page_info['comment_url'] = comment_url + CGI::escape("Development Application Enquiry: " + da_item[headers.index('DA Number')])
  
  page_info
end


das.each do |record|
   if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
     ScraperWiki.save_sqlite(['council_reference'], record)
   else
    puts "Skipping already saved record " + record['council_reference']
   end
end
