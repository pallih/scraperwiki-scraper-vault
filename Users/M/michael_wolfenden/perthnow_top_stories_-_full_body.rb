require 'nokogiri'
require 'uri'
require 'time'

uri = 'http://www.perthnow.com.au/news/top-stories/'
base_uri = URI.parse(uri)

ScraperWiki.sqliteexecute('delete from stories')  

html = ScraperWiki.scrape uri
doc = Nokogiri::HTML html

def clean_text text
  return text.gsub(/^\s+/, '')
             .gsub(/\s+$/, '')
end

doc.search('div.story-block').each do |story|
  heading_link = story.search('h4 a').first
  heading = heading_link.inner_text
  uri = base_uri.merge(heading_link['href']).to_s

  story_html = ScraperWiki.scrape uri
  story_doc = Nokogiri::HTML story_html 
    
  date_and_time = story_doc.search('li.date-and-time').first
  date = date_and_time.search('.datestamp').first.inner_text
  time = date_and_time.search('.timestamp').first.inner_text

  pub_date = Time.parse(Time.parse(date + ' ' + time).to_s.sub('+0000', '+0800'))

  body = ''
  img_src = story_doc.search('div.image-frame img').first
  if (img_src != nil)
    body = '<img src="' + img_src['src']  + '" />'
  end
  
  story_doc.search('div.story-body p').each do |p|
    body = body + '<p>' + clean_text(p.inner_text) + '</p>'
  end

  entry = {
   'heading' => heading,
   'uri' => uri,
   'date' => pub_date,
   'body' => body
  }

  ScraperWiki.save_sqlite(['uri'], entry, 'stories')   
endrequire 'nokogiri'
require 'uri'
require 'time'

uri = 'http://www.perthnow.com.au/news/top-stories/'
base_uri = URI.parse(uri)

ScraperWiki.sqliteexecute('delete from stories')  

html = ScraperWiki.scrape uri
doc = Nokogiri::HTML html

def clean_text text
  return text.gsub(/^\s+/, '')
             .gsub(/\s+$/, '')
end

doc.search('div.story-block').each do |story|
  heading_link = story.search('h4 a').first
  heading = heading_link.inner_text
  uri = base_uri.merge(heading_link['href']).to_s

  story_html = ScraperWiki.scrape uri
  story_doc = Nokogiri::HTML story_html 
    
  date_and_time = story_doc.search('li.date-and-time').first
  date = date_and_time.search('.datestamp').first.inner_text
  time = date_and_time.search('.timestamp').first.inner_text

  pub_date = Time.parse(Time.parse(date + ' ' + time).to_s.sub('+0000', '+0800'))

  body = ''
  img_src = story_doc.search('div.image-frame img').first
  if (img_src != nil)
    body = '<img src="' + img_src['src']  + '" />'
  end
  
  story_doc.search('div.story-body p').each do |p|
    body = body + '<p>' + clean_text(p.inner_text) + '</p>'
  end

  entry = {
   'heading' => heading,
   'uri' => uri,
   'date' => pub_date,
   'body' => body
  }

  ScraperWiki.save_sqlite(['uri'], entry, 'stories')   
end