# coding: utf-8

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'

glossary = ['num', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
 
#glossary = ['x', 'y', 'z']
cur_word = ''
cur_abbr = '' 

# get it terms
glossary.each do |gloss|
  url = "http://www.gartner.com/it-glossary/" + gloss + '/'  
  doc = Nokogiri.HTML(open(url))
  
  doc.search('div[@id="main-content"]/ul/li').each do |v|
    
    if v.at("a").inner_html.strip.split("(").count > 1
      cur_word = v.at("a").inner_html.strip.split("(")[0].strip
      cur_abbr = v.at("a").inner_html.strip.split("(")[1].strip.sub(')', '')
    else
      cur_word = v.at("a").inner_text.strip
      cur_abbr = ''
    end
  
    data = {
      word_link: v.at("a").attributes["href"].value,
      word: cur_word,
      abbr: cur_abbr,
      gloss: v.at("a").inner_text.strip,
      key: gloss
    }   

   #puts data.to_json
   ScraperWiki::save_sqlite(unique_keys=['key','gloss'], data, table_name="it_glossary", verbose=0)
  end
end  

# get OS terms

url = "http://www.computerhope.com/jargon/os.htm"
doc = Nokogiri.HTML(open(url))

doc.search('table[@class="mtable2"]/tr/td/p/a').each do |v|
  
#  p "http://www.computerhope.com/jargon/" + v.attributes["href"].value

  data = {
    word_link: "http://www.computerhope.com/jargon/" + v.attributes["href"].value,
    word: v.inner_html.strip,
    abbr: '',
    gloss: v.inner_html.strip,
    key: v.inner_html.strip.slice!(0)
  }   

 #puts data.to_json
 ScraperWiki::save_sqlite(unique_keys=['key','gloss'], data, table_name="os_glossary", verbose=0)
end


# get database terms

url = "http://databases.about.com/od/administration/a/glossary.htm" 
doc = Nokogiri.HTML(open(url))

doc.search('div[@id="articlebody"]/a').each do |v|
  
#  p v.inner_html.strip
   
  if v.inner_html.strip.split("(").count > 1
    cur_word = v.inner_html.strip.split("(")[0].strip
    cur_abbr = v.inner_html.strip.split("(")[1].strip.sub(')', '')
  else
    cur_word = v.inner_html.strip
    cur_abbr = ''
  end

  data = {
    word_link: v.attributes["href"].value,
    word: cur_word,
    abbr: cur_abbr,
    gloss: v.inner_html.strip,
    key: v.inner_html.strip.slice!(0)
  }   

 #puts data.to_json
 ScraperWiki::save_sqlite(unique_keys=['key','gloss'], data, table_name="database_glossary", verbose=0)
end

