require 'nokogiri'         
require 'open-uri'

doc = Nokogiri::HTML(open("http://beerbloggersconference.org/blogs/complete-list-of-beer-blogs/"))

doc.xpath("//*[@id='content']/div[1]/table[1]/tbody/tr").each do |v|
  cells = v.search 'td'
    data = {
      blog_name: cells[0].inner_html,
      blog_URL: cells[1].search("a/@href")
    }
    ScraperWiki::save_sqlite(['blog_URL'], data)
end


require 'nokogiri'         
require 'open-uri'

doc = Nokogiri::HTML(open("http://beerbloggersconference.org/blogs/complete-list-of-beer-blogs/"))

doc.xpath("//*[@id='content']/div[1]/table[1]/tbody/tr").each do |v|
  cells = v.search 'td'
    data = {
      blog_name: cells[0].inner_html,
      blog_URL: cells[1].search("a/@href")
    }
    ScraperWiki::save_sqlite(['blog_URL'], data)
end


