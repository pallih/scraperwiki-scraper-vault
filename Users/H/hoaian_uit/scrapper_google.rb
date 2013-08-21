require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'json'

def clean_whitespace(a)
   CGI::unescapeHTML(a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip)
end

root = "http://fiverr.com"
link = "http://fiverr.com/gigs/gigs_as_json?host=search&type=longtail&query_string=google%20circles&search_filter=auto&category_id=99912&limit=50&page="

pagecount = 49
while true do
  begin
  go_link = URI.escape(link + pagecount.to_s)
  p go_link

  doc = Nokogiri.HTML(open(go_link))
  JSON.parse(doc.content)['gigs'].each do |item|
    title = item['title_full']
    url = root + "/" + item["gig_url"]
    dsc = ""

    begin
      dsc = clean_whitespace(Nokogiri.HTML(open(url)).css('.gig-main-desc').text)
    rescue
    end
    username = item["seller_name"]
    user_url = root + item["seller_url"]

    record ={
      :title=> title,
      :url=> url,
      :dsc=> dsc,
      :username=> username,
      :user_url=> user_url
    }
    
     if ScraperWiki.select("* from swdata where `url`='#{record['url']}'").empty? 
      ScraperWiki.save_sqlite([], record)
    end
  end
  pagecount += 1
  p pagecount

  rescue Exception => e
    p e
    break
  end
end
require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'json'

def clean_whitespace(a)
   CGI::unescapeHTML(a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip)
end

root = "http://fiverr.com"
link = "http://fiverr.com/gigs/gigs_as_json?host=search&type=longtail&query_string=google%20circles&search_filter=auto&category_id=99912&limit=50&page="

pagecount = 49
while true do
  begin
  go_link = URI.escape(link + pagecount.to_s)
  p go_link

  doc = Nokogiri.HTML(open(go_link))
  JSON.parse(doc.content)['gigs'].each do |item|
    title = item['title_full']
    url = root + "/" + item["gig_url"]
    dsc = ""

    begin
      dsc = clean_whitespace(Nokogiri.HTML(open(url)).css('.gig-main-desc').text)
    rescue
    end
    username = item["seller_name"]
    user_url = root + item["seller_url"]

    record ={
      :title=> title,
      :url=> url,
      :dsc=> dsc,
      :username=> username,
      :user_url=> user_url
    }
    
     if ScraperWiki.select("* from swdata where `url`='#{record['url']}'").empty? 
      ScraperWiki.save_sqlite([], record)
    end
  end
  pagecount += 1
  p pagecount

  rescue Exception => e
    p e
    break
  end
end
