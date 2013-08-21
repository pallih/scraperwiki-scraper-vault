# coding: utf-8

pos = 1
(1..10).each do |p|
  untrusted_string = ScraperWiki::scrape("http://www.tv.com/shows/?pg=#{p}&tag=shows_list;paginator;#{p}")
  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  html = ic.iconv(untrusted_string + ' ')[0..-2]      
  require 'nokogiri'           
  doc = Nokogiri::HTML html
  doc.search("ul.shows .info .title, ul.shows .show .title").each do |v|
    title = v.inner_html.gsub(/[\r\n]/m, '').gsub(/&amp;/, '&').gsub(/<\/?[^>]*>/, "").gsub(/\s+New\!/, '').strip
    data = { :title => title, :index => pos }
    puts data.to_json
    ScraperWiki::save_sqlite(['index', 'title'], data)
    pos += 1
  end
end