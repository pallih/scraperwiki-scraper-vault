# MN Counties

# Description: Grab all MN Counties
# Date:        2/21/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'


url  = "http://www.uscounties.org/cffiles_web/counties/state.cfm?statecode=mn"
html = open(url).read

page     = Nokogiri::HTML(html)
counties = page.css("table")[1].css("tr")

counties[2..-1].each do |county_row|

@data = {
  'name'             =>  county_row.css("td")[0].text.strip,
  'naco_member'      =>  county_row.css("td")[1].text.strip,  
  'population_2000'  =>  county_row.css("td")[2].text.strip,  
  'square_miles'     =>  county_row.css("td")[3].text.strip,
  'seat'             =>  county_row.css("td")[4].text.strip,
  'board_size'       =>  county_row.css("td")[5].text.strip,
  'year_founded'     =>  county_row.css("td")[6].text.strip,

}

ScraperWiki.save(unique_keys = @data.keys, data = @data)


end # counties.each

# MN Counties

# Description: Grab all MN Counties
# Date:        2/21/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'


url  = "http://www.uscounties.org/cffiles_web/counties/state.cfm?statecode=mn"
html = open(url).read

page     = Nokogiri::HTML(html)
counties = page.css("table")[1].css("tr")

counties[2..-1].each do |county_row|

@data = {
  'name'             =>  county_row.css("td")[0].text.strip,
  'naco_member'      =>  county_row.css("td")[1].text.strip,  
  'population_2000'  =>  county_row.css("td")[2].text.strip,  
  'square_miles'     =>  county_row.css("td")[3].text.strip,
  'seat'             =>  county_row.css("td")[4].text.strip,
  'board_size'       =>  county_row.css("td")[5].text.strip,
  'year_founded'     =>  county_row.css("td")[6].text.strip,

}

ScraperWiki.save(unique_keys = @data.keys, data = @data)


end # counties.each

