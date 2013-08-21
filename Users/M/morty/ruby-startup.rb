###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://scraperwiki.com/hello_world.html'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('td').each do |td|
    puts td.inner_html
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)
end
