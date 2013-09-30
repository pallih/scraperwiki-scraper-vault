require "rubygems"
require "open-uri"
require "hpricot"

auctions = []
site = "http://www.bidrivals.com/uk/"
doc = Hpricot(open(site))
elms = doc.search("//div[@class='auction-card float-left float-container relative']")
elms.each do |elm|
  auction = {}
  head = elm.search("h2[@class='title']").search("a").first
  auction["auction"] = head.inner_html
  auction["url"] = head.get_attribute('href')
  auctions << auction
  puts(auction.values.join(","))
end


ScraperWiki.save_sqlite(unique_keys=['auction'],auctions)

require "rubygems"
require "open-uri"
require "hpricot"

auctions = []
site = "http://www.bidrivals.com/uk/"
doc = Hpricot(open(site))
elms = doc.search("//div[@class='auction-card float-left float-container relative']")
elms.each do |elm|
  auction = {}
  head = elm.search("h2[@class='title']").search("a").first
  auction["auction"] = head.inner_html
  auction["url"] = head.get_attribute('href')
  auctions << auction
  puts(auction.values.join(","))
end


ScraperWiki.save_sqlite(unique_keys=['auction'],auctions)

