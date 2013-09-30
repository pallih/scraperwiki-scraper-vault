require "rubygems"
require "open-uri"
require "hpricot"

auctions = []
site = "http://www.quibids.com/en"
doc = Hpricot(open(site))
elms = doc.search("//div[@class='auction-item-wrapper normal']")
elms.each do |elm|
  auction = {}
  link = elm.search("a").first
  auction["auction"] = link.inner_html.gsub(/<br \/>/, "\n")
  auction["url"] = site+"/"+elm.search("a[@href*=/auctions/]").first.get_attribute('href')
  auctions << auction
  puts(auction.values.join(","))
end

ScraperWiki.save_sqlite(unique_keys=['auction'],auctions)

def bidsHistory
  url ="passed arg"
  page = Hpricot(open(url))
  historyTable ={}
  historyTable = page.search("div[@id='bidding-history']")
  rows = historyTable.search("//td")
  bidAmt = rows[0].inner_html
  bidder = rows[1].inner_html
  type = rows[2].inner_html
end

require "rubygems"
require "open-uri"
require "hpricot"

auctions = []
site = "http://www.quibids.com/en"
doc = Hpricot(open(site))
elms = doc.search("//div[@class='auction-item-wrapper normal']")
elms.each do |elm|
  auction = {}
  link = elm.search("a").first
  auction["auction"] = link.inner_html.gsub(/<br \/>/, "\n")
  auction["url"] = site+"/"+elm.search("a[@href*=/auctions/]").first.get_attribute('href')
  auctions << auction
  puts(auction.values.join(","))
end

ScraperWiki.save_sqlite(unique_keys=['auction'],auctions)

def bidsHistory
  url ="passed arg"
  page = Hpricot(open(url))
  historyTable ={}
  historyTable = page.search("div[@id='bidding-history']")
  rows = historyTable.search("//td")
  bidAmt = rows[0].inner_html
  bidder = rows[1].inner_html
  type = rows[2].inner_html
end

