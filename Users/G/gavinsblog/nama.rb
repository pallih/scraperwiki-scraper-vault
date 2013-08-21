require 'scraperwiki'
require 'mechanize'
require 'nokogiri'
require 'open-uri'

jar = Mechanize::CookieJar.new
cookies = Mechanize::Cookie.parse('http://www.nama.ie','pren_terms_accepted=1; expires=Tue, 11 Dec 2022 19:54:31 GMT; path=/; domain=www.nama.ie')
jar << cookies[0]

agent = Mechanize.new {|a| a.user_agent_alias = 'Linux Firefox' }
agent.cookie_jar = jar

url_data = 'http://www.nama.ie/about-our-work/properties-enforced/properties-subject-to-enforcement-action/page/1/?display=all'
data = agent.get(url_data)
data.search('div.pren-property').each do |property|
  title = property.search('h2').first
end

