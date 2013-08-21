# Test scraper for Ruby language.
# Should contain all our documented Ruby functions.
# A fail in this scraper indicates a code failure somewhere.
# TODO: why is this currently failing silently? Failing silently = bad.

require 'nokogiri'

# Monkey-patch for scraping with POST. Does not work.
# TODO: clarify whether we actually want to implement this?
def ScraperWiki.post_scrape (url, params = nil)
   uri  = URI.parse(url)
   if params.nil? 
       data = Net::HTTP.get(uri)
   else
       data = Net::HTTP.post_form(uri, data)
   end
   return data
end

# Scrape function.
html = ScraperWiki.scrape('http://scraperwiki.com/hello_world.html')
puts html
# TODO: POST monkeypatch does not work.
#test_hash = Hash.new
#test_hash["mykey"] = 82
#post_html = ScraperWiki.post_scrape('http://scraperwiki.com/hello_world.html', test_hash)


# Geo function.
latlng = ScraperWiki.gb_postcode_to_latlng("SW1A 1AA")
puts latlng

# Save function with date/latlng objects.
# TODO: figure out appropriate format for latlng save?
doc = Nokogiri::HTML(html)
count = 0
doc.search('td').each do |td|
    count = count + 1
    puts td.inner_html
    record = {}
    record['data']  = td.inner_html
    record['count'] = count
    date = DateTime.now
    ScraperWiki.save(["data"], record, date)
end

# Metadata functions.
metadata_latlng = ScraperWiki.get_metadata("latlng")
puts metadata_latlng
ScraperWiki.save_metadata("latlng",latlng)

