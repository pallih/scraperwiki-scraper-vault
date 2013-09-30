###############################################################################
# Basic scraper
###############################################################################

require 'hpricot'

# retrieve a page
for monthcount in (3..9) do
for daycount in (1..31) do

monthpart = monthcount.to_s()
daypart = daycount.to_s()


linkfirst = 'http://www.flickr.com/services/api/flickr.tags.getRelated.html'
linksecond = '/29/'
startingname = "http://www.flickr.com/photos/imjustwalkin/archives/date-posted/2010/0" + monthpart + "/" + daypart + "/"
starting_url = startingname
#starting_url ='http://www.flickr.com/services/api/flickr.tags.getRelated.html'
html = ScraperWiki.scrape(starting_url)

# use Hpricot to get all <a> tags
doc = Hpricot(html).search('a').search('img')
puts doc
#doc.each do |a|
#    puts a.inner_html
#    record = {'a' => a.inner_html}
#    ScraperWiki.save(['a'], record)
#end

end
end
###############################################################################
# Basic scraper
###############################################################################

require 'hpricot'

# retrieve a page
for monthcount in (3..9) do
for daycount in (1..31) do

monthpart = monthcount.to_s()
daypart = daycount.to_s()


linkfirst = 'http://www.flickr.com/services/api/flickr.tags.getRelated.html'
linksecond = '/29/'
startingname = "http://www.flickr.com/photos/imjustwalkin/archives/date-posted/2010/0" + monthpart + "/" + daypart + "/"
starting_url = startingname
#starting_url ='http://www.flickr.com/services/api/flickr.tags.getRelated.html'
html = ScraperWiki.scrape(starting_url)

# use Hpricot to get all <a> tags
doc = Hpricot(html).search('a').search('img')
puts doc
#doc.each do |a|
#    puts a.inner_html
#    record = {'a' => a.inner_html}
#    ScraperWiki.save(['a'], record)
#end

end
end
