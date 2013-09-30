require 'nokogiri'
pages = 1

def videoURL(page)
  "http://lanyrd.com/video/?page=#{page}"
end

def fetchPage(number)
  html = ScraperWiki.scrape(videoURL(number)) rescue false
  Nokogiri::HTML.parse(html) if html
end

doc = fetchPage(1)
pages = doc.css('.pagination li:last').text.to_i

pages.times do |page|
  doc = fetchPage(page)
  doc.css('.primary .coverage-video').each do |container|
    video = {}
    title = container.css('.title a:first')
    video['title'] = title.text
    video['url'] = title.attr('href').text
    video['meta'] = container.css('.meta').text
    p video
    ScraperWiki.save_sqlite(unique_keys=['url'], data=video)
  end if doc
endrequire 'nokogiri'
pages = 1

def videoURL(page)
  "http://lanyrd.com/video/?page=#{page}"
end

def fetchPage(number)
  html = ScraperWiki.scrape(videoURL(number)) rescue false
  Nokogiri::HTML.parse(html) if html
end

doc = fetchPage(1)
pages = doc.css('.pagination li:last').text.to_i

pages.times do |page|
  doc = fetchPage(page)
  doc.css('.primary .coverage-video').each do |container|
    video = {}
    title = container.css('.title a:first')
    video['title'] = title.text
    video['url'] = title.attr('href').text
    video['meta'] = container.css('.meta').text
    p video
    ScraperWiki.save_sqlite(unique_keys=['url'], data=video)
  end if doc
end