###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://wiki.sasona.org'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('a').each do |a|
    puts a.inner_html
    record = {'a' => a.inner_html}
    ScraperWiki.save(['a'], record)
end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://wiki.sasona.org'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <a> tags
doc = Nokogiri::HTML(html)
doc.search('a').each do |a|
    puts a.inner_html
    record = {'a' => a.inner_html}
    ScraperWiki.save(['a'], record)
end


