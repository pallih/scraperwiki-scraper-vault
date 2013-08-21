require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open("http://www.bergbahn-kitzbuehel.at/en/snow-report.html"))

psb = doc.css('td')[1].content.split(" -  ")
tab = doc.css('td')[7].content.split(" ")
alw = doc.css('td')[16].content.split(" ")
alw.delete_at(0)

ScraperWiki::save_sqlite(
  unique_keys = ["tst"],
  data = {
    "tst"  => Time.now.getutc,
    "pshb" => psb[0],
    "psqb" => psb[1],
    "psht" => doc.css('td')[3].content,
    "sho"  => doc.css('td')[5].content,
    "tabc" => tab[0],
    "tatc" => tab[3],
    "lns"  => doc.css('td')[10].content,
    "ait"  => doc.css('td')[12].content,
    "bpkm" => doc.css('td')[14].content,
    "alws" => alw.join(" ")
  }
)

#puts Time.now.getutc
#puts psb[0]
#puts psb[1]
#puts doc.css('td')[3].content
#puts doc.css('td')[5].content
#puts tab[0]
#puts tab[4]
#puts doc.css('td')[10].content
#puts doc.css('td')[12].content
#puts doc.css('td')[14].content
#puts alw.join(" ")
