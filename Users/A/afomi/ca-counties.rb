# CA Counties

# Description: Grab all CA Counties
# Date:        2/21/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url      = "http://www.uscounties.org/cffiles_web/counties/state.cfm?statecode=ca"
html     = open(url).read
page     = Nokogiri::HTML(html)
counties = page.css("table")[1].css("tr")

counties[2..-1].each do |county|

@data = {
  'name'             =>  county.css("td")[0].text,
  'naco_member'      =>  county.css("td")[1].text,  
  'population_2000'  =>  county.css("td")[2].text,  
  'square_miles'     =>  county.css("td")[3].text,
  'seat'             =>  county.css("td")[4].text,
  'board_size'       =>  county.css("td")[5].text,
  'year_founded'     =>  county.css("td")[6].text,
}

ScraperWiki.save(unique_keys = @data.keys, data = @data)

end # counties.each

# CA Counties

# Description: Grab all CA Counties
# Date:        2/21/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url      = "http://www.uscounties.org/cffiles_web/counties/state.cfm?statecode=ca"
html     = open(url).read
page     = Nokogiri::HTML(html)
counties = page.css("table")[1].css("tr")

counties[2..-1].each do |county|

@data = {
  'name'             =>  county.css("td")[0].text,
  'naco_member'      =>  county.css("td")[1].text,  
  'population_2000'  =>  county.css("td")[2].text,  
  'square_miles'     =>  county.css("td")[3].text,
  'seat'             =>  county.css("td")[4].text,
  'board_size'       =>  county.css("td")[5].text,
  'year_founded'     =>  county.css("td")[6].text,
}

ScraperWiki.save(unique_keys = @data.keys, data = @data)

end # counties.each

