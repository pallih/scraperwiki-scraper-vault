###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page

airport_list = ['MYR', 'GGE', 'CHS', 'CRE']

airport_list.each do |airport|


starting_url = 'http://www.weather.gov/xml/current_obs/K' + airport + '.xml'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <temp_f> tags
doc = Nokogiri::HTML(html)



doc.search('pressure_in').each do |pressure_in|
    puts pressure_in.inner_html
    record = {'pressure_in' => pressure_in.inner_html}
    ScraperWiki.save(['pressure_in'], record)
end
doc.search('temp_f').each do |temp_f|
    puts temp_f.inner_html
    record = {'temp_f' => temp_f.inner_html}
    ScraperWiki.save(['temp_f'], record)
end

end


