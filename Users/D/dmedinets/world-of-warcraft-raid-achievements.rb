###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://us.battle.net/wow/en/character/earthen-ring/tailorpinke/achievement#168'
html = ScraperWiki.scrape(starting_url)

puts html

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
#category_node = doc.css('li').first
#puts "1"
#puts category_node
#puts "2"
doc.css('li').each do |li|
    css_class_name = li.attribute('class').to_s
    next if css_class_name.nil? or css_class_name == ''
    puts css_class_name 
#    record = {'td' => td.inner_html}
#    ScraperWiki.save(['td'], record)
end
