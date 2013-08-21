# Blank Ruby

p "hello! I am coding in the cloud :)"

#html = ScraperWiki::scrape("http://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION^727&insId=2&radius=0.0&displayPropertyType=&minBedrooms=&maxBedrooms=&minPrice=&maxPrice=&maxDaysSinceAdded=&retirement=&sortByPriceDescending=&includeLetAgreed=true&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=false")
#html = ScraperWiki::scrape("http://www.rightmove.co.uk")
#p html

require 'rubygems'
require 'mechanize'
require 'nokogiri'

agent = Mechanize.new

page = agent.get('http://www.rightmove.co.uk')
#p "PRINTING www.rightmove.co.uk"
#pp page



searchLocationForm = page.forms[0]
searchLocationForm.searchLocation = 'Kendal, Cumbria'

# get the button you want from the form
toRentButton = searchLocationForm.button_with(:value => "To Rent")
# submit the form using that button
kendalRentalPage = agent.submit(searchLocationForm, toRentButton)

#page = agent.submit(searchLocationForm)
p "PRINTING forms from results of Kendal rental search"

kendalRentalPage.forms.each do |currentForm|
   p "Kendal search form's fields"
   currentForm.fields.each do |currentField|
      p currentField
   end
end

#Loop through the search forms and set appropriately, distinguishiing by name
#kendalRentalPage.forms.each do |currentForm|
#   if currentForm.name == '_includeLetAgreed'
#      currentForm.value = 'on'
#   end
#end

includeLetAgreedForm = kendalRentalPage.form('_includeLetAgreed')
includeLetAgreedForm.value = 'on'


# get the button you want from the form
#findPropertiesButton = searchLocationForm.button_with(:value => "To Rent")

#kendalRentalDoc = Nokogiri::HTML kendalRentalPage

#p "Kendal Rental Doc div fields"
#kendalRentalDoc.css('div').each do |currentDiv|
#   p currentDiv
#end


#pp kendalRentalPage

#google_form = page.form('f')

#google_form.q = 'ruby mechanize'

#p "PRINTING google form"
#pp google_form

#page = agent.submit(google_form, google_form.buttons.first)

#p "PRINTING search results"
#pp page

#require 'nokogiri'
#doc = Nokogiri::HTML html
#doc.search("div[@align='left'] tr").each do |v|
#  puts v
#  cells = v.search 'td'
#  puts cells
#  if cells.count == 12
#    data = {
#      country: cells[0].inner_html,
#      years_in_school: cells[4].inner_html.to_i
#    }
#    puts data.to_json
#  end
#end

