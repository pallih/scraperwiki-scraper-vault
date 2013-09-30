###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page


starting_url = 'http://api.watershed.co.uk/events'
#html = ScraperWiki.scrape(starting_url)
#@doc = Nokogiri::XML(File.open("shows.xml"))
@doc = Nokogiri::XML(ScraperWiki.scrape(starting_url))

@doc.xpath("//event")

@doc.search('event').each do |td|
  puts td.inner_html
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)
end



# use Nokogiri to get all <td> tags
#doc = Nokogiri::HTML(html)
#doc.search('td').each do |td|
#    puts td.inner_html
#    record = {'td' => td.inner_html}
#    ScraperWiki.save(['td'], record)
#end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page


starting_url = 'http://api.watershed.co.uk/events'
#html = ScraperWiki.scrape(starting_url)
#@doc = Nokogiri::XML(File.open("shows.xml"))
@doc = Nokogiri::XML(ScraperWiki.scrape(starting_url))

@doc.xpath("//event")

@doc.search('event').each do |td|
  puts td.inner_html
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)
end



# use Nokogiri to get all <td> tags
#doc = Nokogiri::HTML(html)
#doc.search('td').each do |td|
#    puts td.inner_html
#    record = {'td' => td.inner_html}
#    ScraperWiki.save(['td'], record)
#end
