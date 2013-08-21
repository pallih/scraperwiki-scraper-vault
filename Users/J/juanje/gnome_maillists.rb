# A GNOME maillists scraper

require 'rubygems'
require 'open-uri'
require 'nokogiri'
require 'tmail'

lists = ['orca-list',
         'gnome-accessibility-devel']
base_url = 'http://mail.gnome.org/archives/'

lists.each do |list|
  puts "List: #{list}"
  url = base_url + list
  doc = Nokogiri::HTML(open url)
  doc.xpath('//tr/td/a').each do |row|
    href = row.attribute('href').value
    puts "\turl: #{href}" if href.include? "txt.gz"
  end
end