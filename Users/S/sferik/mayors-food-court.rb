require 'nokogiri'
require 'uri'

base_url = 'http://www.cityofboston.gov/isd/health/mfc/'
index_page = Nokogiri::HTML(ScraperWiki.scrape(base_url + 'search.asp'))
index_page.css("#Neighborhood option").each do |option|
  neighborhood = option.attributes['value'].value
  next if neighborhood.empty? 
  neighborhood_page = Nokogiri::HTML(ScraperWiki.scrape(URI.encode(base_url + "search.asp?cboNhood=#{neighborhood}&isPostBack=true")))
  neighborhood_page.css("#mainCategoryModuleText a").each do |link|
    puts link.inspect
  end
endrequire 'nokogiri'
require 'uri'

base_url = 'http://www.cityofboston.gov/isd/health/mfc/'
index_page = Nokogiri::HTML(ScraperWiki.scrape(base_url + 'search.asp'))
index_page.css("#Neighborhood option").each do |option|
  neighborhood = option.attributes['value'].value
  next if neighborhood.empty? 
  neighborhood_page = Nokogiri::HTML(ScraperWiki.scrape(URI.encode(base_url + "search.asp?cboNhood=#{neighborhood}&isPostBack=true")))
  neighborhood_page.css("#mainCategoryModuleText a").each do |link|
    puts link.inspect
  end
end