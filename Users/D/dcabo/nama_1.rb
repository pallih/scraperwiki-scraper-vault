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
  agent.get(url).search('div.pren-property').each do |property|
    data = {}

    data[:title] = property.search('h2').text

    about = property.search('div.pren-about')
    items = about.search('p')
    data[:property_type] = items[0].text
    data[:additional_asset_description] = items[1].text

    agent = property.search('div.pren-agent')

    receivers = property.search('div.pren-receivers')

    ScraperWiki.save([:title], data)
  end
end

1.upto(3) do |page_number|
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
  agent.get(url).search('div.pren-property').each do |property|
    data = {}

    data[:title] = property.search('h2').text

    about = property.search('div.pren-about')
    items = about.search('p')
    data[:property_type] = items[0].text
    data[:additional_asset_description] = items[1].text

    agent = property.search('div.pren-agent')

    receivers = property.search('div.pren-receivers')

    ScraperWiki.save([:title], data)
  end
end

1.upto(3) do |page_number|
  url_data = "http://www.nama.ie/about-our-work/properties-enforced/properties-subject-to-enforcement-action/page/#{page_number}/?display=all"
  fetch_page(agent, url_data)
  sleep(2)
end
