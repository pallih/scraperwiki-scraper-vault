# category scraper

require 'nokogiri'

categories = [39, 40, 144, 370, 4082, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 377, 182, 265, 10737, 66, 4356, 25]
maxpage = 20

for category in categories
  page = 1
  while page < maxpage  do

    pageurl = "http://www.skelbiu.lt/skelbimai/bla/bla/#{page}?&category_id=#{category}&orderBy=0"

    puts pageurl

    html = ScraperWiki::scrape(pageurl)
    doc = Nokogiri::HTML(html)   
    
    doc.xpath('//div[@class="simpleAds" or @class="boldAds"]//h3/a/@href').each do |link|
      data = {link: link}
      ScraperWiki::save_sqlite(['link'], data)  
    end

    break unless doc.at_xpath('//*[@id="nextLink"]')

    sleep(4)

    page +=1
  end
end

# category scraper

require 'nokogiri'

categories = [39, 40, 144, 370, 4082, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 377, 182, 265, 10737, 66, 4356, 25]
maxpage = 20

for category in categories
  page = 1
  while page < maxpage  do

    pageurl = "http://www.skelbiu.lt/skelbimai/bla/bla/#{page}?&category_id=#{category}&orderBy=0"

    puts pageurl

    html = ScraperWiki::scrape(pageurl)
    doc = Nokogiri::HTML(html)   
    
    doc.xpath('//div[@class="simpleAds" or @class="boldAds"]//h3/a/@href').each do |link|
      data = {link: link}
      ScraperWiki::save_sqlite(['link'], data)  
    end

    break unless doc.at_xpath('//*[@id="nextLink"]')

    sleep(4)

    page +=1
  end
end

