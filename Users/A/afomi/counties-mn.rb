# Minnesota (MN) Counties
# Description: Grab all MN Counties
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url      = "http://www.uscounties.org/cffiles_web/counties/state.cfm?statecode=mn"
html     = open(url).read
page     = Nokogiri::HTML(html)
counties = page.css("table")[1].css("tr")

counties[2..-1].each do |county|

@data = {
  'name'             =>  county.css("td")[0].text.strip,
  'naco_member'      =>  county.css("td")[1].text.strip,  
  'population_2000'  =>  county.css("td")[2].text.strip,  
  'square_miles'     =>  county.css("td")[3].text.strip,
  'seat'             =>  county.css("td")[4].text.strip,
  'board_size'       =>  county.css("td")[5].text.strip,
  'year_founded'     =>  county.css("td")[6].text.strip,
}

ScraperWiki.save(unique_keys = @data.keys, data = @data)

end # counties.each# Minnesota (MN) Counties
# Description: Grab all MN Counties
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url      = "http://www.uscounties.org/cffiles_web/counties/state.cfm?statecode=mn"
html     = open(url).read
page     = Nokogiri::HTML(html)
counties = page.css("table")[1].css("tr")

counties[2..-1].each do |county|

@data = {
  'name'             =>  county.css("td")[0].text.strip,
  'naco_member'      =>  county.css("td")[1].text.strip,  
  'population_2000'  =>  county.css("td")[2].text.strip,  
  'square_miles'     =>  county.css("td")[3].text.strip,
  'seat'             =>  county.css("td")[4].text.strip,
  'board_size'       =>  county.css("td")[5].text.strip,
  'year_founded'     =>  county.css("td")[6].text.strip,
}

ScraperWiki.save(unique_keys = @data.keys, data = @data)

end # counties.each