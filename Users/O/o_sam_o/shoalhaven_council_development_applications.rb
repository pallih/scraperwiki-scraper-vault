require 'nokogiri'
require 'open-uri'
require 'date'

url = "http://doc.shoalhaven.nsw.gov.au/RSS/SCCRSS.aspx?ID=OpenApps"
doc = Nokogiri::XML(open(url))

comment_url = 'mailto:council@shoalhaven.nsw.gov.au'

das = doc.xpath('//channel/item').collect do |item|
  item = Nokogiri::XML(item.to_xml)
  table = Nokogiri::HTML(item.at_xpath('//description').inner_text)
  table_values = Hash[table.css('tr').collect do |tr|
    tr.css('td').collect { |td| td.inner_text.strip }
  end]
  page_info = {}
  page_info['council_reference'] = item.at_xpath('//title').inner_text.split.first
  page_info['info_url'] = item.at_xpath('//link').inner_text
  page_info['description'] = item.at_xpath('//title').inner_text.split[2..-1].join(' ')
  page_info['date_received'] = Date.strptime(table_values['Date received:'], '%d %B %Y').to_s
  page_info['address'] = table_values['Address:'] + ', NSW'
  page_info['on_notice_to'] = Date.strptime(table_values['Submissions close:'], '%d %B %Y').to_s 
  page_info['date_scraped'] = Date.today.to_s
  page_info['comment_url'] = comment_url
  
  page_info
end

das.each do |record|
   if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true) 
     ScraperWiki.save_sqlite(['council_reference'], record)
   else
     puts "Skipping already saved record " + record['council_reference']
   end
end

require 'nokogiri'
require 'open-uri'
require 'date'

url = "http://doc.shoalhaven.nsw.gov.au/RSS/SCCRSS.aspx?ID=OpenApps"
doc = Nokogiri::XML(open(url))

comment_url = 'mailto:council@shoalhaven.nsw.gov.au'

das = doc.xpath('//channel/item').collect do |item|
  item = Nokogiri::XML(item.to_xml)
  table = Nokogiri::HTML(item.at_xpath('//description').inner_text)
  table_values = Hash[table.css('tr').collect do |tr|
    tr.css('td').collect { |td| td.inner_text.strip }
  end]
  page_info = {}
  page_info['council_reference'] = item.at_xpath('//title').inner_text.split.first
  page_info['info_url'] = item.at_xpath('//link').inner_text
  page_info['description'] = item.at_xpath('//title').inner_text.split[2..-1].join(' ')
  page_info['date_received'] = Date.strptime(table_values['Date received:'], '%d %B %Y').to_s
  page_info['address'] = table_values['Address:'] + ', NSW'
  page_info['on_notice_to'] = Date.strptime(table_values['Submissions close:'], '%d %B %Y').to_s 
  page_info['date_scraped'] = Date.today.to_s
  page_info['comment_url'] = comment_url
  
  page_info
end

das.each do |record|
   if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true) 
     ScraperWiki.save_sqlite(['council_reference'], record)
   else
     puts "Skipping already saved record " + record['council_reference']
   end
end

