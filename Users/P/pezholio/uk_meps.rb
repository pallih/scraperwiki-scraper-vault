require 'mechanize'
require 'nokogiri'

def titleize(str)
  str.gsub(/\w+/) do |word|
    word.capitalize
  end
end

BASE_URL = 'http://www.europarl.europa.eu'

url = BASE_URL + '/meps/en/performsearch.html'

agent = Mechanize.new

page = agent.get(url)

doc = Nokogiri.HTML(page.content)

countries = doc.search('select[@id="searchmenu_country"]//optgroup[@label="United Kingdom"]//option')

countries.shift

countries.each do |country|

  data = {
    'termId' => 7,
    'name' => nil,
    'politicalGroup' => nil,
    'webCountry' => country[:value],
    'bodyType' => 'ALL',
    'search' => 'Show result'
  }
  
  page = agent.post(url, data)
  
  doc = Nokogiri.HTML(page.content)
  
  meps = doc.search('.ep_block .ep_elementpeople1')
  
  meps.each do |mep|
    
    details = {}
    
    details[:name] = titleize(mep.search('.ep_title')[0].inner_text.strip)
    details[:region] = country[:value].gsub('*', '')
    details[:url] = BASE_URL + mep.search('.ep_title')[0][:href]
    details[:group] = mep.search('.ep_europeaninfo .ep_group')[0].children.first.text.strip
    details[:party] = mep.search('.ep_nationalinfo .ep_group')[0].inner_text.strip
    details[:image] = BASE_URL + mep.search('.ep_img img')[0][:src]

    info_page = agent.get(details[:url])

    info_doc = Nokogiri.HTML(info_page.content)
    
    details[:email] = mep.search('.ep_title')[0][:href].scan(/\/meps\/en\/[0-9]+\/([^.]+).html/)[0][0].gsub(" ", "").gsub("_", ".").downcase.gsub("(theearlof)", "") + "@europarl.europa.eu" # Emails are obsfucated, but they follow the same scheme as URLs
    details[:website] = info_doc.search('.ep_website a')[0][:href] rescue nil
    details[:rss] = BASE_URL + info_doc.search('.ep_rss a')[0][:href]
    details[:tel1] = info_doc.search('.ep_elementcontact .ep_phone')[0].inner_text.strip
    details[:tel2] = info_doc.search('.ep_elementcontact .ep_phone')[1].inner_text.strip
    details[:fax1] = info_doc.search('.ep_elementcontact .ep_fax')[0].inner_text.strip
    details[:fax2] = info_doc.search('.ep_elementcontact .ep_fax')[1].inner_text.strip
    details[:address1] = info_doc.search('.ep_elementcontact .ep_address')[0].inner_text.strip
    details[:address2] = info_doc.search('.ep_elementcontact .ep_address')[1].inner_text.strip
    details[:address3] = info_doc.search('.ep_elementcontact .ep_address')[2].inner_text.strip
    
    ScraperWiki.save([:name], details)
    
  end
end