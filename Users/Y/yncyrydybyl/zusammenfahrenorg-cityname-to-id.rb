# coding: utf-8
# Blank Ruby
# used to map id for zusammenfahren.org
# http://www.zusammenfahren.org/suchen.php
require "nokogiri"
require 'iconv'

def convert_encoding(html)
  index_doc = Nokogiri::HTML(html)
  encoding = index_doc.meta_encoding()
  encoding = "ISO-8859-15"
  if encoding
    puts encoding
    #puts "bad füssingen"
    ic = Iconv.new('UTF-8',encoding)
    html = ic.iconv(html)
  end
  return html
end
def scrape_and_convert_to_utf8(url)
  html = ScraperWiki.scrape(url)
  return convert_encoding(html)
end

url = "http://www.zusammenfahren.org/suchen.php"
page = Nokogiri::HTML(scrape_and_convert_to_utf8(url))

page.search("select[name=los] option")[22..22].each do |option|
   #puts option.attr("value")
   #puts option.content
   city = option.content
   #city = Iconv.conv("UTF8","iso-8859", option.content)
   #city = option.content
   puts city.to_json
   city = Iconv.conv("UTF-8","iso-8859-2", city)
   puts city
   ScraperWiki.save_sqlite(unique_keys=['city'], data={"city"=>city, "id"=>option.attr("value")})
  

end
# coding: utf-8
# Blank Ruby
# used to map id for zusammenfahren.org
# http://www.zusammenfahren.org/suchen.php
require "nokogiri"
require 'iconv'

def convert_encoding(html)
  index_doc = Nokogiri::HTML(html)
  encoding = index_doc.meta_encoding()
  encoding = "ISO-8859-15"
  if encoding
    puts encoding
    #puts "bad füssingen"
    ic = Iconv.new('UTF-8',encoding)
    html = ic.iconv(html)
  end
  return html
end
def scrape_and_convert_to_utf8(url)
  html = ScraperWiki.scrape(url)
  return convert_encoding(html)
end

url = "http://www.zusammenfahren.org/suchen.php"
page = Nokogiri::HTML(scrape_and_convert_to_utf8(url))

page.search("select[name=los] option")[22..22].each do |option|
   #puts option.attr("value")
   #puts option.content
   city = option.content
   #city = Iconv.conv("UTF8","iso-8859", option.content)
   #city = option.content
   puts city.to_json
   city = Iconv.conv("UTF-8","iso-8859-2", city)
   puts city
   ScraperWiki.save_sqlite(unique_keys=['city'], data={"city"=>city, "id"=>option.attr("value")})
  

end
