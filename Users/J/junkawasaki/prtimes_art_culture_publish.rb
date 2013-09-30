# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'kconv'


# html = ScraperWiki::scrape("http://prtimes.jp/main/html/searchbiscate/busi_cate_id/007") # => this is return null value

# data[] = {'url', 'title', 'body', 'created'}
datas = []

5.times { |i| 
  doc = Nokogiri::HTML(open("http://prtimes.jp/main/html/searchbiscate/busi_cate_id/007/busi_cate_lv2_id/0/pagenum/#{i}"))
  doc.search("div#main div.b1 ul li").each do  |article|
    datas << {
      'url' => "http://prtimes.jp" + article.search("div.data h2 a").first[:href],
      'title' => article.search("div.data h2 a").text,
      'body' => article.search("div.data p.release_text").text,
      'date' => article.search("div.data p.date").text
    }
  end
}

begin
  scraperwiki.sqlite.execute(" create table article ( id INTEGER PRIMARY KEY AUTOINCREMENT )")
rescue
  puts "table property already exists;"
end

ScraperWiki::save_sqlite(unique_keys=["url"], datas, table_name='article')# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'kconv'


# html = ScraperWiki::scrape("http://prtimes.jp/main/html/searchbiscate/busi_cate_id/007") # => this is return null value

# data[] = {'url', 'title', 'body', 'created'}
datas = []

5.times { |i| 
  doc = Nokogiri::HTML(open("http://prtimes.jp/main/html/searchbiscate/busi_cate_id/007/busi_cate_lv2_id/0/pagenum/#{i}"))
  doc.search("div#main div.b1 ul li").each do  |article|
    datas << {
      'url' => "http://prtimes.jp" + article.search("div.data h2 a").first[:href],
      'title' => article.search("div.data h2 a").text,
      'body' => article.search("div.data p.release_text").text,
      'date' => article.search("div.data p.date").text
    }
  end
}

begin
  scraperwiki.sqlite.execute(" create table article ( id INTEGER PRIMARY KEY AUTOINCREMENT )")
rescue
  puts "table property already exists;"
end

ScraperWiki::save_sqlite(unique_keys=["url"], datas, table_name='article')