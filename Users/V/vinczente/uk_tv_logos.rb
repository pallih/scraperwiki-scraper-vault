# Blank Ruby
# encoding: UTF-8

require 'mechanize'
require 'nokogiri'
require 'iconv'
require 'open-uri'
require 'digest/md5'

url = 'http://www.lyngsat-logo.com/tvcountry/uk.html'
html = ScraperWiki.scrape(url)
ic_ignore = Iconv.new('UTF-8//IGNORE', 'UTF-8')
html = ic_ignore.iconv(html)
page = Nokogiri::HTML(html)

page.at("table").search('tr').each do |r|
  if(r.search('td')[0]!=nil)
  r.search('td').each do |s|
    if (s.search('img')[0] !=nil)
    if s.search('img')[0]['src'].include? "icon"
      puts s.search('a')[1].inner_html
      record = {
      'name'=> s.search('a')[1].inner_html,
      'url' => s.search('img')[0]['src'].gsub('..','http://www.lyngsat-logo.com'),
      'key' => Digest::MD5.hexdigest(s.search('a')[1].inner_html)
      }
      ScraperWiki.save_sqlite(['key'], record)
    end
    end
  end
  end
end# Blank Ruby
# encoding: UTF-8

require 'mechanize'
require 'nokogiri'
require 'iconv'
require 'open-uri'
require 'digest/md5'

url = 'http://www.lyngsat-logo.com/tvcountry/uk.html'
html = ScraperWiki.scrape(url)
ic_ignore = Iconv.new('UTF-8//IGNORE', 'UTF-8')
html = ic_ignore.iconv(html)
page = Nokogiri::HTML(html)

page.at("table").search('tr').each do |r|
  if(r.search('td')[0]!=nil)
  r.search('td').each do |s|
    if (s.search('img')[0] !=nil)
    if s.search('img')[0]['src'].include? "icon"
      puts s.search('a')[1].inner_html
      record = {
      'name'=> s.search('a')[1].inner_html,
      'url' => s.search('img')[0]['src'].gsub('..','http://www.lyngsat-logo.com'),
      'key' => Digest::MD5.hexdigest(s.search('a')[1].inner_html)
      }
      ScraperWiki.save_sqlite(['key'], record)
    end
    end
  end
  end
end