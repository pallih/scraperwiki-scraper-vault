# Blank Ruby
require 'scraperwiki'
require 'nokogiri'

html = ScraperWiki::scrape('http://www.informit.com/index.aspx')
doc = Nokogiri::HTML(html, nil, 'utf-8') # encoding very important!!!
p html
ebookDetails =  doc.css('.details')
title = ebookDetails.css('.title').text
img = "http://www.informit.com" + ebookDetails.css('.product').attr('src')
link = "http://www.informit.com" + ebookDetails.css('.buy').attr('href')

#p title
#p img
#p link

ScraperWiki::save_sqlite(['title'], { title: title, img: img, link: link, date: DateTime.now }) 
