# Blank Ruby
# encoding: utf-8

require 'uri'
require 'open-uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'

@title = Array.new
@meta_description = Array.new
@price = Array.new
@header = Array.new
@description = Array.new
@image = Array.new

def scrape(a, b)
base="http://www.skates.co.uk"
  puts a+b
  agent = Mechanize.new
  agent.get(a)

  begin
    event = agent.page.at('div[@class="template_main"]')
  rescue
    puts('Nav Page')
  end

event.xpath('//title').each do |title|
    @title << title.inner_html
  end

event.xpath("//meta[@name='description']/@content").each do |meta_desc|
      @meta_description << meta_desc.content
  end

event.css('.details_price_now').each do |price|
      @price << price.inner_text
  end

event.search('h1').each do |h1|
    @header << h1.inner_text
  end

event.search('//*[@class="details_attributes"]').each {|x| x.remove}
event.search('//*[@class="details_tabs_large ui-tabs ui-widget ui-widget-content ui-corner-all"]').each {|x1| x1.remove}
event.search('//*[@id="details_delivery_tab"]').each {|x2| x2.remove}
event.search('//*[@class="details_grey"]').each {|x3| x3.remove}
event.search('//*[@class="details_actions"]').each {|x4| x4.remove}
event.search('//*[@class="details_promo_box"]').each {|x5| x5.remove}

event.css('.details_right').each do |details|
    @description << details.inner_text
  end

event.xpath('//*[@id="zoom1"]//img/@src').each do |img_src|
    @image << img_src.to_s
  end

(0..@title.length - 1).each do |index|
    puts "title: #{@title[index]}"
    puts "meta description: #{@meta_description[index]}"    
    puts "price: #{@price[index]}"
    puts "header: #{@header[index]}"
    puts "description: #{@description[index]}"
    puts "image: #{@image[index]}"
    puts ""
  end

(0..@title.length - 1).each do |index|
ScraperWiki.save_sqlite(unique_keys=['url'], data= {'url' => a }, table_name='crawled_urls')
ScraperWiki.save_sqlite(unique_keys=['url'], data= {'url' => a, 'title' => @title[index], 'meta_desc' => @meta_description[index], 'price' => @price[index], 'header' => @header[index], 'description' => @description[index], 'image' => @image[index]}, table_name='pages')
end
end

  site="http://www.skates.co.uk/scooters/"
  base="http://www.skates.co.uk"

  agent = Mechanize.new
  agent.get(site)
  doc = agent.page.at('html body')
  nodes = agent.page.search('.productlist_grid h2 a, ul.productlist_paging a' )

  for link in nodes
    evurl = base + link.attributes['href']
    # scrape(evurl, '?currency=GBP')
    data = { 'queue_url' => evurl }
      ScraperWiki.save_sqlite(unique_keys=['queue_url'], data=data, table_name='links')
  end

scraped = []
ScraperWiki.sqliteexecute("select * from links where not like * from crawled_urls").each do |row|
   scrape = scraped.push(row[0])
end
# Blank Ruby
# encoding: utf-8

require 'uri'
require 'open-uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'

@title = Array.new
@meta_description = Array.new
@price = Array.new
@header = Array.new
@description = Array.new
@image = Array.new

def scrape(a, b)
base="http://www.skates.co.uk"
  puts a+b
  agent = Mechanize.new
  agent.get(a)

  begin
    event = agent.page.at('div[@class="template_main"]')
  rescue
    puts('Nav Page')
  end

event.xpath('//title').each do |title|
    @title << title.inner_html
  end

event.xpath("//meta[@name='description']/@content").each do |meta_desc|
      @meta_description << meta_desc.content
  end

event.css('.details_price_now').each do |price|
      @price << price.inner_text
  end

event.search('h1').each do |h1|
    @header << h1.inner_text
  end

event.search('//*[@class="details_attributes"]').each {|x| x.remove}
event.search('//*[@class="details_tabs_large ui-tabs ui-widget ui-widget-content ui-corner-all"]').each {|x1| x1.remove}
event.search('//*[@id="details_delivery_tab"]').each {|x2| x2.remove}
event.search('//*[@class="details_grey"]').each {|x3| x3.remove}
event.search('//*[@class="details_actions"]').each {|x4| x4.remove}
event.search('//*[@class="details_promo_box"]').each {|x5| x5.remove}

event.css('.details_right').each do |details|
    @description << details.inner_text
  end

event.xpath('//*[@id="zoom1"]//img/@src').each do |img_src|
    @image << img_src.to_s
  end

(0..@title.length - 1).each do |index|
    puts "title: #{@title[index]}"
    puts "meta description: #{@meta_description[index]}"    
    puts "price: #{@price[index]}"
    puts "header: #{@header[index]}"
    puts "description: #{@description[index]}"
    puts "image: #{@image[index]}"
    puts ""
  end

(0..@title.length - 1).each do |index|
ScraperWiki.save_sqlite(unique_keys=['url'], data= {'url' => a }, table_name='crawled_urls')
ScraperWiki.save_sqlite(unique_keys=['url'], data= {'url' => a, 'title' => @title[index], 'meta_desc' => @meta_description[index], 'price' => @price[index], 'header' => @header[index], 'description' => @description[index], 'image' => @image[index]}, table_name='pages')
end
end

  site="http://www.skates.co.uk/scooters/"
  base="http://www.skates.co.uk"

  agent = Mechanize.new
  agent.get(site)
  doc = agent.page.at('html body')
  nodes = agent.page.search('.productlist_grid h2 a, ul.productlist_paging a' )

  for link in nodes
    evurl = base + link.attributes['href']
    # scrape(evurl, '?currency=GBP')
    data = { 'queue_url' => evurl }
      ScraperWiki.save_sqlite(unique_keys=['queue_url'], data=data, table_name='links')
  end

scraped = []
ScraperWiki.sqliteexecute("select * from links where not like * from crawled_urls").each do |row|
   scrape = scraped.push(row[0])
end
