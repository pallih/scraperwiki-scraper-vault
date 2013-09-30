require 'open-uri'
require 'nokogiri'
require 'net/http'
require 'ostruct'
require 'mechanize'

j=2904263904714727
while j<9999999999999999
 
 queryurl='http://www.indeed.com/p/jobsite.php?pid='+j.to_s()
  #puts queryurl
  doc = Nokogiri::HTML(open(queryurl))
  doc.search("div[@class='INDEED']").each do |node|
      puts j
         data={
            id: j,
            name: "unknown"
          }
         ScraperWiki::save_sqlite(['id'], data)
    end
  j=j+1
  endrequire 'open-uri'
require 'nokogiri'
require 'net/http'
require 'ostruct'
require 'mechanize'

j=2904263904714727
while j<9999999999999999
 
 queryurl='http://www.indeed.com/p/jobsite.php?pid='+j.to_s()
  #puts queryurl
  doc = Nokogiri::HTML(open(queryurl))
  doc.search("div[@class='INDEED']").each do |node|
      puts j
         data={
            id: j,
            name: "unknown"
          }
         ScraperWiki::save_sqlite(['id'], data)
    end
  j=j+1
  end