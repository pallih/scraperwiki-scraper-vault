require 'open-uri'
require 'nokogiri'

url = 'http://newschallenge.tumblr.com/page/'

(1..90).each do |i|
  page = url + "#{i}"
  html = Nokogiri::HTML(open(page))
  html.css('.posts > .postbox').each do |post|
    unless post.blank? 
      listing         = {}
      if post.at_css('h2') == nil
        listing[:title] = ''
      else
        listing[:title] = "#{post.at_css('h2').text}"
      end
      listing[:url]   = "#{post.at_css('a.home-view')['href']}" 
      listing[:likes] = "#{post.at_css('.home-likes').text}".to_i
      ScraperWiki.save(['url'], listing)
    end
  end
end