require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open("http://www.w3schools.com/browsers/browsers_stats.asp"))

latest = doc.css('td')[1].content
ymo = doc.css('th')[0].content + " " + doc.css('td')[0].content
iex = doc.css('td')[1].content
ffx = doc.css('td')[2].content
chr = doc.css('td')[3].content
saf = doc.css('td')[4].content
ope = doc.css('td')[5].content

ScraperWiki::save_sqlite(
  unique_keys = ["ymo"],
  data = {
    "ymo" => ymo,
    "tst" => Time.now.getutc,
    "iex" => iex,
    "ffx" => ffx,
    "chr" => chr,
    "saf" => saf,
    "ope" => ope
  }
)

#puts ymo
#puts Time.now.getutc
#puts iex
#puts ffx
#puts chr
#puts saf
#puts ope
require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open("http://www.w3schools.com/browsers/browsers_stats.asp"))

latest = doc.css('td')[1].content
ymo = doc.css('th')[0].content + " " + doc.css('td')[0].content
iex = doc.css('td')[1].content
ffx = doc.css('td')[2].content
chr = doc.css('td')[3].content
saf = doc.css('td')[4].content
ope = doc.css('td')[5].content

ScraperWiki::save_sqlite(
  unique_keys = ["ymo"],
  data = {
    "ymo" => ymo,
    "tst" => Time.now.getutc,
    "iex" => iex,
    "ffx" => ffx,
    "chr" => chr,
    "saf" => saf,
    "ope" => ope
  }
)

#puts ymo
#puts Time.now.getutc
#puts iex
#puts ffx
#puts chr
#puts saf
#puts ope
