###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.publications.parliament.uk/pa/cm/cmfbusi/a01.htm'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('.paraFutureBusinessDate').each do |td|
    puts td.inner_html
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)
end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.publications.parliament.uk/pa/cm/cmfbusi/a01.htm'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('.paraFutureBusinessDate').each do |td|
    puts td.inner_html
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)
end
