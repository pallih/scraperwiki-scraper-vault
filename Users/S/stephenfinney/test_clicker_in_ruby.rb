require 'rubygems'
require 'scraperwiki'
require 'mechanize'
require 'nokogiri'

agent = Mechanize.new

page = agent.get('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275')

page.links.each do |link|
  puts link.text
end

page = agent.page.link_with(:text => 'next').click
#pp page
#page = agent.page.link_with(:href => 'javascript:ShowPage(20)').click
require 'rubygems'
require 'scraperwiki'
require 'mechanize'
require 'nokogiri'

agent = Mechanize.new

page = agent.get('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275')

page.links.each do |link|
  puts link.text
end

page = agent.page.link_with(:text => 'next').click
#pp page
#page = agent.page.link_with(:href => 'javascript:ShowPage(20)').click
require 'rubygems'
require 'scraperwiki'
require 'mechanize'
require 'nokogiri'

agent = Mechanize.new

page = agent.get('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275')

page.links.each do |link|
  puts link.text
end

page = agent.page.link_with(:text => 'next').click
#pp page
#page = agent.page.link_with(:href => 'javascript:ShowPage(20)').click
