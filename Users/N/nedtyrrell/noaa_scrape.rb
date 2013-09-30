###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page

airport_list = ['PDX', 'ORD', 'LGA']

airport_list.each do |airport|


starting_url = 'http://www.weather.gov/xml/current_obs/K' + airport + '.xml'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <temp_f> tags
doc = Nokogiri::HTML(html)



doc.search('temp_f').each do |temp_f|
    puts temp_f.inner_html
    record = {'temp_f' => temp_f.inner_html}
    ScraperWiki.save(['temp_f'], record)
end

end

###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page

airport_list = ['PDX', 'ORD', 'LGA']

airport_list.each do |airport|


starting_url = 'http://www.weather.gov/xml/current_obs/K' + airport + '.xml'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <temp_f> tags
doc = Nokogiri::HTML(html)



doc.search('temp_f').each do |temp_f|
    puts temp_f.inner_html
    record = {'temp_f' => temp_f.inner_html}
    ScraperWiki.save(['temp_f'], record)
end

end

