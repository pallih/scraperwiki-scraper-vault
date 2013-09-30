# Scrape list of ScraperWiki scrapers

list_url = "http://api.scraperwiki.com/api/1.0/scraper/search?format=jsondict&maxrows=1000000"
detail_url = "http://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&version=-1&name="

# search for empty string to get all scrapers
json = ScraperWiki.scrape(list_url)
puts json
scrapers = JSON.parse(json)

for scraper in scrapers
  # read extra detail info
  json2 = ScraperWiki.scrape(detail_url + scraper['short_name'])
  puts json2
  extra = JSON.parse(json2)[0]
  scraper['records'] = extra['records']

  # save to the datastore
  ScraperWiki.save(unique_keys=['short_name'], data=scraper)
end


# Scrape list of ScraperWiki scrapers

list_url = "http://api.scraperwiki.com/api/1.0/scraper/search?format=jsondict&maxrows=1000000"
detail_url = "http://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&version=-1&name="

# search for empty string to get all scrapers
json = ScraperWiki.scrape(list_url)
puts json
scrapers = JSON.parse(json)

for scraper in scrapers
  # read extra detail info
  json2 = ScraperWiki.scrape(detail_url + scraper['short_name'])
  puts json2
  extra = JSON.parse(json2)[0]
  scraper['records'] = extra['records']

  # save to the datastore
  ScraperWiki.save(unique_keys=['short_name'], data=scraper)
end


