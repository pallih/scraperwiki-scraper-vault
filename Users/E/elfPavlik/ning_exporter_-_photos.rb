#Scraping photos from money-free.ning.com
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://money-free.ning.com/photo'
agent = Mechanize.new

# Scraping logic for a single page
def scrape_page(page)
  page.search('h3 a').each do |photo_page_link|
    html = ScraperWiki.scrape(photo_page_link['href'])
    doc = Nokogiri::HTML(html)
    puts doc.css('h1').text
    puts doc.css('.ib a').first['href']
    puts doc.css('.byline li:nth-child(1)').text
    puts doc.css('.xg_sprite-view-fullsize').first['href']
    puts doc.css('#tagsList').text
    puts doc.css('.object-detail').text
    puts doc.css('#comments dd').size
  end
end

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(agent)
    scrape_page(agent.page)
    link = agent.page.link_with(:text => 'Next ›')
    if link
      link.click
      scrape_and_look_for_next_link(agent)
    end
end

# Do scraping
agent.get(BASE_URL)
scrape_and_look_for_next_link(agent)

#Scraping photos from money-free.ning.com
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://money-free.ning.com/photo'
agent = Mechanize.new

# Scraping logic for a single page
def scrape_page(page)
  page.search('h3 a').each do |photo_page_link|
    html = ScraperWiki.scrape(photo_page_link['href'])
    doc = Nokogiri::HTML(html)
    puts doc.css('h1').text
    puts doc.css('.ib a').first['href']
    puts doc.css('.byline li:nth-child(1)').text
    puts doc.css('.xg_sprite-view-fullsize').first['href']
    puts doc.css('#tagsList').text
    puts doc.css('.object-detail').text
    puts doc.css('#comments dd').size
  end
end

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(agent)
    scrape_page(agent.page)
    link = agent.page.link_with(:text => 'Next ›')
    if link
      link.click
      scrape_and_look_for_next_link(agent)
    end
end

# Do scraping
agent.get(BASE_URL)
scrape_and_look_for_next_link(agent)

