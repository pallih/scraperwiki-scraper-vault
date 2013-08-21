###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.boxofficemojo.com/people/?view=Actor&pagenum=1&sort=sumgross&order=DESC&&p=.htm'
html = ScraperWiki.scrape(starting_url)
puts html

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('td').each do |td|
    puts td.inner_html
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)
end
