require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'net/http'
require 'digest/md5'


## setup
base_url= "http://www.berlinerbaederbetriebe.de/"
initial_page= "12.html?&no_cache=1" # distributor page, links to various pool types
ua = 'Lynx/2.8.7rel.2 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.0a'
rundate = Time.now

## start
a = Mechanize.new
a.user_agent = ua
doc = a.get "#{base_url}#{initial_page}"

# determine on which subpages we'll find swimming pools
subpages = []
doc.search("//*[@id='content_left']/p/a/@href").each do |v|
subpages << v.text
end
subpages.uniq! # there may be dupes

# looping thru subpages

subpages.each do |i|
  doc = a.get "#{base_url}#{i}"
    doc.search("//*[@id='content']/p/a").each do |j|
      
 
# puts "#{j.text.strip} extern" if j.text.strip.include?('*')
 bname = j.text.strip.gsub("*","")
 is_external = j.text.strip.include?('*') 

# create md5-hashed categories from cat. icons
uri = URI(base_url + j.children[1].first[1])
category_image = Net::HTTP.get(uri)
digest = Digest::MD5.hexdigest(category_image)
 
 
   data = {
          category_digest: digest,
          pool_name: bname,
          detail_url: base_url + j['href'],
          external_operator:  is_external,       
          icon_url: base_url + j.children[1].first[1],
          last_run: rundate }

          ScraperWiki::save_sqlite(['pool_name'], data)      
          #puts data.to_json
       
      end
  end



require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'net/http'
require 'digest/md5'


## setup
base_url= "http://www.berlinerbaederbetriebe.de/"
initial_page= "12.html?&no_cache=1" # distributor page, links to various pool types
ua = 'Lynx/2.8.7rel.2 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.0a'
rundate = Time.now

## start
a = Mechanize.new
a.user_agent = ua
doc = a.get "#{base_url}#{initial_page}"

# determine on which subpages we'll find swimming pools
subpages = []
doc.search("//*[@id='content_left']/p/a/@href").each do |v|
subpages << v.text
end
subpages.uniq! # there may be dupes

# looping thru subpages

subpages.each do |i|
  doc = a.get "#{base_url}#{i}"
    doc.search("//*[@id='content']/p/a").each do |j|
      
 
# puts "#{j.text.strip} extern" if j.text.strip.include?('*')
 bname = j.text.strip.gsub("*","")
 is_external = j.text.strip.include?('*') 

# create md5-hashed categories from cat. icons
uri = URI(base_url + j.children[1].first[1])
category_image = Net::HTTP.get(uri)
digest = Digest::MD5.hexdigest(category_image)
 
 
   data = {
          category_digest: digest,
          pool_name: bname,
          detail_url: base_url + j['href'],
          external_operator:  is_external,       
          icon_url: base_url + j.children[1].first[1],
          last_run: rundate }

          ScraperWiki::save_sqlite(['pool_name'], data)      
          #puts data.to_json
       
      end
  end



