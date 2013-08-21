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


#ScraperWiki::sqliteexecute("update search_keyword set Provider = keyword where Provider is null")
#ScraperWiki::commit()



#glossary = ['num', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
 
glossary = ['x', 'y', 'z']
cur_word = ''
cur_abbr = '' 

# webopedia
# http://www.webopedia.com/Top_Category.asp

url = 'http://www.abv.bg'
#url = "http://www.webopedia.com/Top_Category.asp"  
doc = Nokogiri.HTML(open(url))

#ScraperWiki::sqliteexecute("delete from webopedia_glossary where 1=1")

doc.search('div[@class="subcat-list"]/div/ul/li').each do |v|
  
#  p v.at("a").inner_html.strip  + ' : http://www.webopedia.com' +  v.at("a").attributes["href"].value


  if v.at("a").inner_html.strip.start_with?("<img border=") == false
    category = v.at("a").inner_html.strip
    url_inner = 'http://www.webopedia.com' +  v.at("a").attributes["href"].value
    sub_category = v.at("a").attributes["href"].value.split("/")[1].strip
#    category = v.at("a").attributes["href"].value.split("/")[2].strip

#    p sub_category + ' : ' + category

    doc_inner = Nokogiri.HTML(open(url_inner)) rescue doc_inner = v

    
    doc_inner.search('div[@class="browse-list"]/div/ul/li').each do |vv|
      cat_attrib = vv.at("a").attributes["class"].value rescue cat_attrib = ""
      
      if cat_attrib != "category"
#        p vv.at("a").inner_html.strip  + ' :: http://www.webopedia.com' +  vv.at("a").attributes["href"].value
        term = vv.at("a").inner_html.strip
        url_term = "http://www.webopedia.com" +  vv.at("a").attributes["href"].value
        key = vv.at("a").attributes["href"].value.split("/")[2].strip rescue key = ''

#        doc_term = Nokogiri.HTML(open(url_term)) rescue doc_term = vv
        gloss_text = ''
        gloss_html = ''
#        gloss_text = v.search 'div[@class="term termmargin"]'
#        gloss_text = v.search 'div[@class="term termmargin"]'[0].inner_text.strip rescue gloss_text = ''
#        gloss_html = v.search 'div[@class="term termmargin"]'[0].inner_html rescue gloss_html = ''
    
        data = {
          sub_category: sub_category,
          category: category,
          url_category: url_inner,
          gloss: term,
          url_gloss: url_term,
          gloss_text: gloss_text,
          gloss_html: gloss_html,
          key: key
        }   

        #puts data.to_json
        ScraperWiki::save_sqlite(unique_keys=['key', 'category'], data, table_name="webopedia_glossary", verbose=0)
        ScraperWiki::commit()
      end
    end
  else
    cur_word = ''
    cur_abbr = ''
  end
end


if 1 > 0 then
 
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

end #if 1 > 2




# MIT
# http://kb.mit.edu/confluence/labels/listlabels-alphaview.action
# http://kb.mit.edu/confluence/labels/listlabels-alphaview.action
