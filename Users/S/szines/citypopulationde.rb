require 'nokogiri'
require 'mechanize'
require 'pp'

website = "http://www.citypopulation.de/USA.html"
html = ScraperWiki::scrape(website)
doc = Nokogiri::HTML html

urlset = Hash.new

doc.search("table[class='select'] tr").each do |v|
  cells = v.search 'a'
#  pp cells.to_json
#  pp cells.count
  if cells.count > 3
      data = {
                href: cells[3][:href],
                content: cells[3].content
                }
      pp data
urlset = urlset.merge(data)
pp urlset
  end
end

pp urlset

def datascraper(url)
  pageurl = 'http://www.citypopulation.de/'+url
  puts pageurl
  html = ScraperWiki::scrape(pageurl)
  doc = Nokogiri::HTML html

  doc.search("table[id='ts'] tr").each do |v|
    cells = v.search 'td'
    if cells.count > 0
      data = {
              content: cells[0].content,
         
              }
      ScraperWiki::save_sqlite(['content'], data)
    end
   end
end

datascraper(urlset[1]['href'])require 'nokogiri'
require 'mechanize'
require 'pp'

website = "http://www.citypopulation.de/USA.html"
html = ScraperWiki::scrape(website)
doc = Nokogiri::HTML html

urlset = Hash.new

doc.search("table[class='select'] tr").each do |v|
  cells = v.search 'a'
#  pp cells.to_json
#  pp cells.count
  if cells.count > 3
      data = {
                href: cells[3][:href],
                content: cells[3].content
                }
      pp data
urlset = urlset.merge(data)
pp urlset
  end
end

pp urlset

def datascraper(url)
  pageurl = 'http://www.citypopulation.de/'+url
  puts pageurl
  html = ScraperWiki::scrape(pageurl)
  doc = Nokogiri::HTML html

  doc.search("table[id='ts'] tr").each do |v|
    cells = v.search 'td'
    if cells.count > 0
      data = {
              content: cells[0].content,
         
              }
      ScraperWiki::save_sqlite(['content'], data)
    end
   end
end

datascraper(urlset[1]['href'])