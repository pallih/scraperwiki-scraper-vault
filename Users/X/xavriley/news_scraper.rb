# Blank Ruby
require 'nokogiri'

# @base_url = "http://www.hdh.co.uk/press/"

@base_url = "http://www.hdh.co.uk/news/archive/"

# date_range = 2005..2012

date_range = 2009..2012

date_range.each do |news_year|
  puts "Starting Scrape of #{news_year}"
  html = ScraperWiki.scrape(@base_url + news_year.to_s)

  docCat = Nokogiri::HTML(html)
  
  unless news_year == 2011
  docCat.css('td a').each { |story|
    story_url = story.attr('href').to_s
    p @base_url  + news_year.to_s + '/' +story_url
    if story_url =~ /\.html/ 
      p story_url
      story_html = ScraperWiki.scrape(@base_url + news_year.to_s + '/' + story_url)
      story_data = Nokogiri::HTML(story_html)
    
      data = Hash.new
      p story_data.inspect
      data['date_string'] = story_data.css('p.title').inner_html
      data['title'] = story_data.css('p.article_body strong').inner_html.to_s
      p data['title']
      data['body'] = story_data.css('#content').inner_html.to_s.gsub(story_data.css('#flash_holder_1').inner_html.to_s, '').gsub('<div id="flash_holder_1"></div>', '').strip
      ScraperWiki.save_sqlite(unique_keys=['title'], data=data)
    end
  }
  end

end
