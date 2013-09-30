# Housing in Toronto
require 'nokogiri'
require 'open-uri'
require 'mechanize'
require 'rubygems'

$BASEURL = 'http://tampa.craigslist.org/cto'
$MAX_DEPTH = 50 #scrapes no more than 10 pages

=begin
#http://toronto.en.craigslist.ca/off/
#http://toronto.en.craigslist.ca/sub/
html = open(url)
doc = Nokogiri::HTML(html)
cities = ['ottawa']
listings = doc.css("p").map { |node| 
  { 
    'url' => URI.parse(node.at_css("a").attribute("href")),
    'content' => node.at_css("a").content
    #traverse through and put the reply-to email there
  }
}
listings.each do |listing|
  listing['destination'] = (listing['content'].downcase[/(#{cities.join("|")})/] || "N/A").gsub("nyc", "new york")
end
ScraperWiki.save_sqlite(unique_keys=['url'], data=listings)
=end

$brw = Mechanize.new { |b|
b.user_agent_alias ='Linux Firefox'
b.read_timeout = 1200
}


def scrape(pageurl,searchdepth)
  if searchdepth <= $MAX_DEPTH

    #look for all links containing information
    page = $brw.get(pageurl)
    pg = page.search(".//p[@class='row']/a")
    
    #puts pg.inspect
    pg.each do |link|
      #puts link
      #puts link.xpath('@href')
      #puts link.text
  
      ln = link.xpath('@href')
      #scrape the reply-to address from
      replyln = $brw.get(ln).search(".//a[@href[contains(.,'mailto')]]")
      unless replyln.empty? 
        ScraperWiki.save_sqlite(unique_keys=['url'], data={'url'=>ln,'text'=>link.text,'email'=>replyln.text})
      end
    end
    #go to next page
    np = page.search(".//p[@id='nextpage']//a[@href[contains(.,'index')]]")
    unless np.empty? 
      scrape($BASEURL + np.xpath('@href').text,searchdepth+1)
    end
  end
end

scrape($BASEURL,1)
# Housing in Toronto
require 'nokogiri'
require 'open-uri'
require 'mechanize'
require 'rubygems'

$BASEURL = 'http://tampa.craigslist.org/cto'
$MAX_DEPTH = 50 #scrapes no more than 10 pages

=begin
#http://toronto.en.craigslist.ca/off/
#http://toronto.en.craigslist.ca/sub/
html = open(url)
doc = Nokogiri::HTML(html)
cities = ['ottawa']
listings = doc.css("p").map { |node| 
  { 
    'url' => URI.parse(node.at_css("a").attribute("href")),
    'content' => node.at_css("a").content
    #traverse through and put the reply-to email there
  }
}
listings.each do |listing|
  listing['destination'] = (listing['content'].downcase[/(#{cities.join("|")})/] || "N/A").gsub("nyc", "new york")
end
ScraperWiki.save_sqlite(unique_keys=['url'], data=listings)
=end

$brw = Mechanize.new { |b|
b.user_agent_alias ='Linux Firefox'
b.read_timeout = 1200
}


def scrape(pageurl,searchdepth)
  if searchdepth <= $MAX_DEPTH

    #look for all links containing information
    page = $brw.get(pageurl)
    pg = page.search(".//p[@class='row']/a")
    
    #puts pg.inspect
    pg.each do |link|
      #puts link
      #puts link.xpath('@href')
      #puts link.text
  
      ln = link.xpath('@href')
      #scrape the reply-to address from
      replyln = $brw.get(ln).search(".//a[@href[contains(.,'mailto')]]")
      unless replyln.empty? 
        ScraperWiki.save_sqlite(unique_keys=['url'], data={'url'=>ln,'text'=>link.text,'email'=>replyln.text})
      end
    end
    #go to next page
    np = page.search(".//p[@id='nextpage']//a[@href[contains(.,'index')]]")
    unless np.empty? 
      scrape($BASEURL + np.xpath('@href').text,searchdepth+1)
    end
  end
end

scrape($BASEURL,1)
