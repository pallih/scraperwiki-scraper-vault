require 'nokogiri'

html = ScraperWiki.scrape("http://www6.hawaii.gov/dot/administration/contracts/bidopening/bidcurrent.htm")
doc = Nokogiri::HTML(html)
all_bids = {}
curr_id = ""

doc.css('table tr table tr table tr').each do |row|
  cells = row.css('td')
  attr_name = cells[0].inner_text.strip.downcase.gsub(/\s+/, '').delete(':')
  attribute = cells[1].inner_text.strip
  curr_id = attribute if attr_name.include?("projectno")
  # puts curr_id
  # puts "#{attr_name} = #{attribute}"
  all_bids["#{curr_id}"] = {} if all_bids["#{curr_id}"].nil? 
  all_bids["#{curr_id}"]["#{attr_name}"] = attribute
end

all_bids.each do |bid|
  bidinfo = bid[1]
  ScraperWiki.save_sqlite(unique_keys=['projectno'], data=bidinfo)
  p bidinfo
end

require 'nokogiri'

html = ScraperWiki.scrape("http://www6.hawaii.gov/dot/administration/contracts/bidopening/bidcurrent.htm")
doc = Nokogiri::HTML(html)
all_bids = {}
curr_id = ""

doc.css('table tr table tr table tr').each do |row|
  cells = row.css('td')
  attr_name = cells[0].inner_text.strip.downcase.gsub(/\s+/, '').delete(':')
  attribute = cells[1].inner_text.strip
  curr_id = attribute if attr_name.include?("projectno")
  # puts curr_id
  # puts "#{attr_name} = #{attribute}"
  all_bids["#{curr_id}"] = {} if all_bids["#{curr_id}"].nil? 
  all_bids["#{curr_id}"]["#{attr_name}"] = attribute
end

all_bids.each do |bid|
  bidinfo = bid[1]
  ScraperWiki.save_sqlite(unique_keys=['projectno'], data=bidinfo)
  p bidinfo
end

