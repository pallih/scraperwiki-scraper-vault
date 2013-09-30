# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'kconv'

# html = ScraperWiki::scrape("http://prtimes.jp/main/html/searchbiscate/busi_cate_id/007") # => this is return null value

# data[] = {'url', 'title', 'body', 'created'}
datas = []

begin
  scraperwiki.sqlite.execute("create table article ( id INTEGER PRIMARY KEY AUTOINCREMENT )")
rescue
  puts "table property already exists;"
end

current_code = ScraperWiki::select("id from article order by id DESC limit 1")

for i in current_code[0]['id']...15118
  doc = Nokogiri::XML(open("http://cdn.animenewsnetwork.com/encyclopedia/api.xml?title=#{i}"))
  title_ja = doc.xpath("//info[@type='Alternative title' and @lang='JA'][last()]").text
 
  puts i
  puts title_ja

  data = {
      'id' => i,
      'japanese_name' => title_ja,
   }

  ScraperWiki::save_sqlite(unique_keys=["id"], data, table_name='article')
end# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'kconv'

# html = ScraperWiki::scrape("http://prtimes.jp/main/html/searchbiscate/busi_cate_id/007") # => this is return null value

# data[] = {'url', 'title', 'body', 'created'}
datas = []

begin
  scraperwiki.sqlite.execute("create table article ( id INTEGER PRIMARY KEY AUTOINCREMENT )")
rescue
  puts "table property already exists;"
end

current_code = ScraperWiki::select("id from article order by id DESC limit 1")

for i in current_code[0]['id']...15118
  doc = Nokogiri::XML(open("http://cdn.animenewsnetwork.com/encyclopedia/api.xml?title=#{i}"))
  title_ja = doc.xpath("//info[@type='Alternative title' and @lang='JA'][last()]").text
 
  puts i
  puts title_ja

  data = {
      'id' => i,
      'japanese_name' => title_ja,
   }

  ScraperWiki::save_sqlite(unique_keys=["id"], data, table_name='article')
end