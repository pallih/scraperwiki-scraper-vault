require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'net/http'

root = "http://fiverr.com"
link = "http://fiverr.com/gigs/gigs_as_json?host=search&type=longtail&query_string=twitter%20followers&search_filter=auto&category_id=99912&limit=50&page="

pagecount = 61
while true do
  begin
  uri = URI.escape(link + pagecount.to_s)
  
  url = URI.parse(uri)
  req = Net::HTTP::Get.new(url.path)
  res = Net::HTTP.start(url.host, url.port) {|http|
    http.request(req)
  }
  puts res.body

  doc = Nokogiri.HTML(c)

  JSON.parse(doc.content)['gigs'].each do |item|
    title = item['title_full']
    url = root + "/" + item["gig_url"]
    dsc = clean_whitespace(Nokogiri.HTML(open( url)).css('.gig-main-desc').text)
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
require 'net/http'

root = "http://fiverr.com"
link = "http://fiverr.com/gigs/gigs_as_json?host=search&type=longtail&query_string=twitter%20followers&search_filter=auto&category_id=99912&limit=50&page="

pagecount = 61
while true do
  begin
  uri = URI.escape(link + pagecount.to_s)
  
  url = URI.parse(uri)
  req = Net::HTTP::Get.new(url.path)
  res = Net::HTTP.start(url.host, url.port) {|http|
    http.request(req)
  }
  puts res.body

  doc = Nokogiri.HTML(c)

  JSON.parse(doc.content)['gigs'].each do |item|
    title = item['title_full']
    url = root + "/" + item["gig_url"]
    dsc = clean_whitespace(Nokogiri.HTML(open( url)).css('.gig-main-desc').text)
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
require 'net/http'

root = "http://fiverr.com"
link = "http://fiverr.com/gigs/gigs_as_json?host=search&type=longtail&query_string=twitter%20followers&search_filter=auto&category_id=99912&limit=50&page="

pagecount = 61
while true do
  begin
  uri = URI.escape(link + pagecount.to_s)
  
  url = URI.parse(uri)
  req = Net::HTTP::Get.new(url.path)
  res = Net::HTTP.start(url.host, url.port) {|http|
    http.request(req)
  }
  puts res.body

  doc = Nokogiri.HTML(c)

  JSON.parse(doc.content)['gigs'].each do |item|
    title = item['title_full']
    url = root + "/" + item["gig_url"]
    dsc = clean_whitespace(Nokogiri.HTML(open( url)).css('.gig-main-desc').text)
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
require 'net/http'

root = "http://fiverr.com"
link = "http://fiverr.com/gigs/gigs_as_json?host=search&type=longtail&query_string=twitter%20followers&search_filter=auto&category_id=99912&limit=50&page="

pagecount = 61
while true do
  begin
  uri = URI.escape(link + pagecount.to_s)
  
  url = URI.parse(uri)
  req = Net::HTTP::Get.new(url.path)
  res = Net::HTTP.start(url.host, url.port) {|http|
    http.request(req)
  }
  puts res.body

  doc = Nokogiri.HTML(c)

  JSON.parse(doc.content)['gigs'].each do |item|
    title = item['title_full']
    url = root + "/" + item["gig_url"]
    dsc = clean_whitespace(Nokogiri.HTML(open( url)).css('.gig-main-desc').text)
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
