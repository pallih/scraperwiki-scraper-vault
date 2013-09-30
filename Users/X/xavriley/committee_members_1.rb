# Blank Ruby
require 'cgi'
require 'uri'
require 'open-uri'
puts "Starting Scrape of Committee Members"

(1..32).each do |pageno|

html = ScraperWiki.scrape("http://www.balderton.com/news-events/news-archive/#{pageno}")

require 'nokogiri'           

docCat = Nokogiri::HTML(html)
data = Hash.new

members = docCat.css('div.news').each { |member|
  data['news_title'] = member.at('h2 a').text
  @news_url = member.at('h2 a').attr('href').to_s.gsub(',', '%2C')
  data['news_url'] = @news_url
  data['news_date'] = member.at('.l p.first').text
  data['news_company'] = member.css('.l p')[1].text
  data['news_author'] = member.css('.l p')[2].text
  data['news_summary'] = member.at('p.body').text

  connectHtml = "http://www.balderton.com#{@news_url}"
  mainHtml = ScraperWiki.scrape(connectHtml) rescue 'There was an error fetching ' + @news_url
  docBody = Nokogiri::HTML(mainHtml)
  unless docBody.at('.news p.body').nil? then data['news_body'] = docBody.at('.news p.body').text end
  unless docBody.at('.news div a img').nil? then data['news_logo'] = docBody.at('.news div a img').attr('src').to_s end

  ScraperWiki.save_sqlite(unique_keys=['news_url'], data=data)
  
  #data = Array.new
  #mainHtml = ''
}

end# Blank Ruby
require 'cgi'
require 'uri'
require 'open-uri'
puts "Starting Scrape of Committee Members"

(1..32).each do |pageno|

html = ScraperWiki.scrape("http://www.balderton.com/news-events/news-archive/#{pageno}")

require 'nokogiri'           

docCat = Nokogiri::HTML(html)
data = Hash.new

members = docCat.css('div.news').each { |member|
  data['news_title'] = member.at('h2 a').text
  @news_url = member.at('h2 a').attr('href').to_s.gsub(',', '%2C')
  data['news_url'] = @news_url
  data['news_date'] = member.at('.l p.first').text
  data['news_company'] = member.css('.l p')[1].text
  data['news_author'] = member.css('.l p')[2].text
  data['news_summary'] = member.at('p.body').text

  connectHtml = "http://www.balderton.com#{@news_url}"
  mainHtml = ScraperWiki.scrape(connectHtml) rescue 'There was an error fetching ' + @news_url
  docBody = Nokogiri::HTML(mainHtml)
  unless docBody.at('.news p.body').nil? then data['news_body'] = docBody.at('.news p.body').text end
  unless docBody.at('.news div a img').nil? then data['news_logo'] = docBody.at('.news div a img').attr('src').to_s end

  ScraperWiki.save_sqlite(unique_keys=['news_url'], data=data)
  
  #data = Array.new
  #mainHtml = ''
}

end