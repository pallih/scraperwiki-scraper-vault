###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.bbc.co.uk/iplayer/tv/categories/films'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('.episode-info a').each do |episode|
    record = {'title' => episode['title'], 'href' => "http://www.bbc.co.uk" + episode['href']}
    ScraperWiki.save(['title'], record)
end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.bbc.co.uk/iplayer/tv/categories/films'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('.episode-info a').each do |episode|
    record = {'title' => episode['title'], 'href' => "http://www.bbc.co.uk" + episode['href']}
    ScraperWiki.save(['title'], record)
end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.bbc.co.uk/iplayer/tv/categories/films'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
doc.search('.episode-info a').each do |episode|
    record = {'title' => episode['title'], 'href' => "http://www.bbc.co.uk" + episode['href']}
    ScraperWiki.save(['title'], record)
end
