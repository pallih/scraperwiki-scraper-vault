###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://wiki.sasona.org/SasonaPublicWorkstations'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get the content from the "content" div tag
doc = Nokogiri::HTML(html)
doc.xpath("id('content')").each do |div|
    puts div.inner_html
    record = {'div' => div.inner_html}
    ScraperWiki.save(['div'], record)
end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://wiki.sasona.org/SasonaPublicWorkstations'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get the content from the "content" div tag
doc = Nokogiri::HTML(html)
doc.xpath("id('content')").each do |div|
    puts div.inner_html
    record = {'div' => div.inner_html}
    ScraperWiki.save(['div'], record)
end
