html = ScraperWiki.scrape("http://cbtcws.cityofhouston.gov/ActiveIncidents//Combined.aspx");

require 'nokogiri'

doc = Nokogiri::HTML(html);

# doc.xpath('//body/form/div/table/tbody/tr/td/table/tbody/tr').each do |row|
doc.xpath('//table[@class="bltable"]//tr').each do |row|
  
  department = row.xpath('td')[0].content.tr("\t\r\n", '')
  elements = row.xpath('td/font').map do |elem| elem.content.tr("\t\r\n", ''); end
  combined_response = row.xpath('td')[6].content.tr("\t\r\n", '')
  
  next if(department[0..5] == 'Agency')
  
  data = {
    'department' => department,
    'address' => elements[0],
    'cross_street' => elements[1],
    'key_map' => elements[2],
    'call_time' => elements[3],
    'incident_type' => elements[4],
    'combined_response' => combined_response
  }

  puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['address', 'cross_street'], data=data)
end

html = ScraperWiki.scrape("http://cbtcws.cityofhouston.gov/ActiveIncidents//Combined.aspx");

require 'nokogiri'

doc = Nokogiri::HTML(html);

# doc.xpath('//body/form/div/table/tbody/tr/td/table/tbody/tr').each do |row|
doc.xpath('//table[@class="bltable"]//tr').each do |row|
  
  department = row.xpath('td')[0].content.tr("\t\r\n", '')
  elements = row.xpath('td/font').map do |elem| elem.content.tr("\t\r\n", ''); end
  combined_response = row.xpath('td')[6].content.tr("\t\r\n", '')
  
  next if(department[0..5] == 'Agency')
  
  data = {
    'department' => department,
    'address' => elements[0],
    'cross_street' => elements[1],
    'key_map' => elements[2],
    'call_time' => elements[3],
    'incident_type' => elements[4],
    'combined_response' => combined_response
  }

  puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['address', 'cross_street'], data=data)
end

