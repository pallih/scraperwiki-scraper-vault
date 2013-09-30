# Housing in Vancuver
require 'nokogiri'
require 'open-uri'
require 'mechanize'
require 'rubygems'

$BASEURL = 'http://vancouver.en.craigslist.ca/apa/'
$MAX_DEPTH = 50 #scrapes no more than 10 pages

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
# Housing in Vancuver
require 'nokogiri'
require 'open-uri'
require 'mechanize'
require 'rubygems'

$BASEURL = 'http://vancouver.en.craigslist.ca/apa/'
$MAX_DEPTH = 50 #scrapes no more than 10 pages

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
