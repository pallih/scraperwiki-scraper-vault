require 'scraperwiki'
require 'mechanize'
require 'nokogiri'
require 'open-uri'

jar = Mechanize::CookieJar.new
cookies = Mechanize::Cookie.parse('http://www.nama.ie','pren_terms_accepted=1; expires=Tue, 11 Dec 2022 19:54:31 GMT; path=/; domain=www.nama.ie')
jar << cookies[0]

agent = Mechanize.new {|a| a.user_agent_alias = 'Linux Firefox' }
agent.cookie_jar = jar

def fetch_page(agent, url)
  properties = agent.get(url).search('div.pren-property')
  # puts "Fetching page ...#{url[-30..-1]}, got #{properties.size} results..."
  properties.each do |property|
    data = {}

    data[:id] = property.attributes['id']
    data[:title] = property.search('h2').text

    about = property.search('div.pren-about')
    items = about.search('p')
    data[:property_type] = items[0].text
    data[:additional_asset_description] = items[1].text
    data[:completed_units] = items[2].text
    data[:link_to_brochure] = items[3].text 

    sales_agent = property.search('div.pren-agent')
    items = sales_agent.search('p')
    data[:sales_firm_name] = items[0].text
    data[:sales_phone_number] = items[1].text
    data[:sales_email_address] = items[2].text
    
    receivers = property.search('div.pren-receivers')
    items = receivers.search('p')
    data[:receivers_firm] = items[0].text
    data[:receivers_email_address] = items[1].text
    data[:receivers_phone_number] = items[2].text

    ScraperWiki.save([:id], data)
  end
end

1.upto(150) do |page_number|
  url_data = "http://www.nama.ie/about-our-work/properties-enforced/properties-subject-to-enforcement-action/page/#{page_number}/?display=all"
  fetch_page(agent, url_data)
  sleep(2)
end
require 'scraperwiki'
require 'mechanize'
require 'nokogiri'
require 'open-uri'

jar = Mechanize::CookieJar.new
cookies = Mechanize::Cookie.parse('http://www.nama.ie','pren_terms_accepted=1; expires=Tue, 11 Dec 2022 19:54:31 GMT; path=/; domain=www.nama.ie')
jar << cookies[0]

agent = Mechanize.new {|a| a.user_agent_alias = 'Linux Firefox' }
agent.cookie_jar = jar

def fetch_page(agent, url)
  properties = agent.get(url).search('div.pren-property')
  # puts "Fetching page ...#{url[-30..-1]}, got #{properties.size} results..."
  properties.each do |property|
    data = {}

    data[:id] = property.attributes['id']
    data[:title] = property.search('h2').text

    about = property.search('div.pren-about')
    items = about.search('p')
    data[:property_type] = items[0].text
    data[:additional_asset_description] = items[1].text
    data[:completed_units] = items[2].text
    data[:link_to_brochure] = items[3].text 

    sales_agent = property.search('div.pren-agent')
    items = sales_agent.search('p')
    data[:sales_firm_name] = items[0].text
    data[:sales_phone_number] = items[1].text
    data[:sales_email_address] = items[2].text
    
    receivers = property.search('div.pren-receivers')
    items = receivers.search('p')
    data[:receivers_firm] = items[0].text
    data[:receivers_email_address] = items[1].text
    data[:receivers_phone_number] = items[2].text

    ScraperWiki.save([:id], data)
  end
end

1.upto(150) do |page_number|
  url_data = "http://www.nama.ie/about-our-work/properties-enforced/properties-subject-to-enforcement-action/page/#{page_number}/?display=all"
  fetch_page(agent, url_data)
  sleep(2)
end
