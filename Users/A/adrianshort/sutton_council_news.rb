# TODO Handle images in the sidebar

require 'nokogiri'
require 'pp'
require 'date'

RSS_URL = "http://www.sutton.gov.uk/index.aspx?articleid=5292" # Latest news RSS feed
BASE_URL = "http://www.sutton.gov.uk/"

#---------------------------------------------------------------

def scrape_article(url)
  doc = Nokogiri.HTML(ScraperWiki.scrape(url))

  data = {}

  unless article = doc.at("#cc")
    puts "Couldn't find div#cc element in #{url}"
    return {}
  end

  # Grab the image from the sidebar (if any) and insert it at the top of the article body
  if img = doc.at("#rhc img")
    unless img[:src].match(/^https?/)
      img['src'] = BASE_URL + img['src'].sub(/^\.\//, '')
    end
    data[:image_url] =     img[:src]
    data[:image_title] =   img[:title]
    data[:image_width] =   img[:width]
    data[:image_height] =  img[:height]
    article.at("#introtext").before(img) # insert the img element into the doc before #introtext
  end

  # Remove the two links at the bottom of the article that are within the div#cc and the <br> between them
  article.search(".subscribe").remove
  article.search("br").last.remove
  article.at("a[@style='text-decoration: underline;']").remove

  h1 = article.at("h1")
  headline = h1.inner_text.strip

  # Some articles don't have dates, e.g. http://www.sutton.gov.uk/index.aspx?articleid=14922
  published_date = headline.match(/(\d{1,2}\.\d{1,2}\.\d{2})/).to_s

  if published_date > ""
    pubdate = Date.strptime(published_date, "%d.%m.%y")
    headline.sub!(published_date, '')
    headline.sub!(/\s*-\s*$/, '') # remove dash at end with optional spaces around it
    data[:pubdate] = pubdate.strftime("%Y-%m-%d")
  end

  h1.remove
  data[:headline] = headline
  data[:summary] = article.at("#introtext").inner_text.strip
  
  # Convert relative to absolute URLs in links
  article.search("a").each do |anchor|
    unless anchor['href'].match(/^(https?|mailto|ftp|tel|callto|webcal)/)
      anchor['href'] = BASE_URL + anchor['href'].sub(/^\.\//, '')
    end
  end

  # Convert relative to absolute URLs in images
  article.search("img").each do |image|
    unless image['src'].match(/^https?/)
      image['src'] = BASE_URL + image['src'].sub(/^\.\//, '')
    end
  end

  data[:body] = article.inner_html.strip
  data
end

#---------------------------------------------------------------

doc = Nokogiri.XML(ScraperWiki.scrape(RSS_URL))
puts "RSS feed fetched OK"

doc.css("item link").each do |link|
  data = {}
  data[:id] =  link.inner_text.match(/articleid=(\d+)/).captures[0].to_i
  data[:url] = link.inner_text.strip
  pp data
  data.merge!(scrape_article(data[:url]))
  data[:updated_at] = Time.now.to_s
  ScraperWiki.save_sqlite([:id], data)
  sleep 10
end
