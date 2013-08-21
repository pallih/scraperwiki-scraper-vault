# encoding: utf-8
require 'nokogiri'
require 'yaml'
$debug=nil
url="http://ibnlive.in.com/videos/show/v/Devil's-Advocate.html"
data=ScraperWiki.scrape(url)

doc=Nokogiri::HTML(data)

items = (doc/("div#video_box1")).search("li")
puts "Parsed #{items.length} items" if $debug
puts "Type: #{items.class}" if $debug
r=%r{^.*/videos/(\d+)/.*}
items.each{|i|
  data={}
  link="http://ibnlive.in.com/"+i.at("a")[:href]
  puts "Link = #{link}" if $debug
  data['link'] = link
  img = i.at("div.imgs_v").at("img")[:src]
  puts "img = #{img}" if $debug
  data['img'] = img
  headline= (i/"div.txt1").inner_text
  puts "headline: #{headline}" if $debug
  data['headline'] = headline
  data['title']=data['headline']
  desc = "<a href='#{data['link']}'><img src='#{data['img']}'/>#{data['headline']}</a>"
  puts "Description: #{desc}" if $debug
  data['description'] = desc
  tm = Date.parse(i.at("div.dt").inner_text.split.join(' ')).strftime("%Y-%m-%dT00:01:00+05:30")
  puts "Time: #{tm}" if $debug
  data['time'] = tm
  data['pubDate'] = tm
  m = r.match(data['link'])
  if m
    data['videoid'] = (m)[1]
    puts data.to_json if $debug
    ScraperWiki.save_sqlite(unique_keys=['videoid'], data=data)
  end
}
