###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.imdb.com/title/tt0052520/episodes'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('.filter-all h3, .filter-all h3 a').each do |h3|
    puts h3.inner_html
    record = {'h3' => h3.inner_html}
    ScraperWiki.save(['h3'], record)
end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.imdb.com/title/tt0052520/episodes'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('.filter-all h3, .filter-all h3 a').each do |h3|
    puts h3.inner_html
    record = {'h3' => h3.inner_html}
    ScraperWiki.save(['h3'], record)
end
