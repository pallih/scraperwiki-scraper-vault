# Blank Ruby


require 'mechanize'
require 'nokogiri'
require 'open-uri'




def scrape_page(html)
begin
@record = {}
doc = Nokogiri::HTML(html)

results = doc.css('li.item').collect do |item|
  name = item.css('div.organization-title').inner_text.strip
  email = item.css('div.email span.content-email a').inner_text.strip
  phone = item.css('div.phone span.content-phone').inner_text.strip
  address = item.css('div.adress span.content-address').inner_text.strip
  description = item.css('div.organization_details').inner_text.strip

puts name
puts email
puts phone
puts address
puts description

@record['contact_company']  = name
@record['contact_phone']  =  phone
@record['contact_address']  =  address
@record['contact_email']  =  email
@record['contact_department']  =  description

ScraperWiki.save(['contact_email'], @record)

end

@record = {}
results = doc.css('li.item-alt').collect do |item|
  name = item.css('div.organization-title').inner_text.strip
  email = item.css('div.email span.content-email a').inner_text.strip
  phone = item.css('div.phone span.content-phone').inner_text.strip
  address = item.css('div.adress span.content-address').inner_text.strip
  description = item.css('div.organization_details').inner_text.strip

puts name
puts email
puts phone
puts address
puts description

@record['contact_company']  = name
@record['contact_phone']  =  phone
@record['contact_address']  =  address
@record['contact_email']  =  email
@record['contact_department']  =  description

ScraperWiki.save(['contact_email'], @record)

end



rescue Timeout::Error
retry
rescue => e
puts e.class
end

end

def submit_form
begin
agent = Mechanize.new
agent.get('http://www.ingaa.org/Foundation/FoundationMembers.aspx')
form = agent.page.forms.first
puts form.fields[11].value
form.fields[11].value=(-1)
puts form.fields[11].value
puts form.buttons.last.name
response = form.click_button(form.button_with(:name => 'ctl03$ctl57$btnApplyFilters'))


@html = response.body
puts @html

rescue Timeout::Error
retry
rescue => e
puts e.class
end
end

submit_form
scrape_page(@html)

# Blank Ruby


require 'mechanize'
require 'nokogiri'
require 'open-uri'




def scrape_page(html)
begin
@record = {}
doc = Nokogiri::HTML(html)

results = doc.css('li.item').collect do |item|
  name = item.css('div.organization-title').inner_text.strip
  email = item.css('div.email span.content-email a').inner_text.strip
  phone = item.css('div.phone span.content-phone').inner_text.strip
  address = item.css('div.adress span.content-address').inner_text.strip
  description = item.css('div.organization_details').inner_text.strip

puts name
puts email
puts phone
puts address
puts description

@record['contact_company']  = name
@record['contact_phone']  =  phone
@record['contact_address']  =  address
@record['contact_email']  =  email
@record['contact_department']  =  description

ScraperWiki.save(['contact_email'], @record)

end

@record = {}
results = doc.css('li.item-alt').collect do |item|
  name = item.css('div.organization-title').inner_text.strip
  email = item.css('div.email span.content-email a').inner_text.strip
  phone = item.css('div.phone span.content-phone').inner_text.strip
  address = item.css('div.adress span.content-address').inner_text.strip
  description = item.css('div.organization_details').inner_text.strip

puts name
puts email
puts phone
puts address
puts description

@record['contact_company']  = name
@record['contact_phone']  =  phone
@record['contact_address']  =  address
@record['contact_email']  =  email
@record['contact_department']  =  description

ScraperWiki.save(['contact_email'], @record)

end



rescue Timeout::Error
retry
rescue => e
puts e.class
end

end

def submit_form
begin
agent = Mechanize.new
agent.get('http://www.ingaa.org/Foundation/FoundationMembers.aspx')
form = agent.page.forms.first
puts form.fields[11].value
form.fields[11].value=(-1)
puts form.fields[11].value
puts form.buttons.last.name
response = form.click_button(form.button_with(:name => 'ctl03$ctl57$btnApplyFilters'))


@html = response.body
puts @html

rescue Timeout::Error
retry
rescue => e
puts e.class
end
end

submit_form
scrape_page(@html)

