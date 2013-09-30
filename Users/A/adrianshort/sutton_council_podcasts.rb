require 'nokogiri'
require 'time'
require 'pp'

FEED_TITLE = "Cheam North and Worcester Park Local Committee"
FEED_IMAGE = "https://dl.dropbox.com/u/300783/sutton-council-logo-1600-sq.jpg"
FEED_AUTHOR = "London Borough of Sutton"
FEED_LINK = "https://www.sutton.gov.uk/index.aspx?articleid=4332"

sourcescraper = 'cheam-north-worcester-park-local-committee-podcast'

ScraperWiki::attach(sourcescraper)

items = ScraperWiki::select("* from swdata order by d desc limit 50")

builder = Nokogiri::XML::Builder.new do |xml|
  xml.rss('xmlns:itunes' => "http://www.itunes.com/dtds/podcast-1.0.dtd", :version => "2.0") {
    xml.channel {
      xml.title FEED_TITLE
      xml.link FEED_LINK
      xml['itunes'].image(:href => FEED_IMAGE)
      xml['itunes'].author FEED_AUTHOR
 
      items.each do |i|
        xml.item {
          xml.title i['title']
          xml['itunes'].author FEED_AUTHOR
          xml.enclosure(:url => i['href'], :type => "audio/mpeg")
          xml.guid i['href']
          xml.pubDate Time.parse(i['d']).rfc822
        }
      end
    }
  }
end

ScraperWiki::httpresponseheader("Content-Type", "application/rss+xml")
puts builder.to_xmlrequire 'nokogiri'
require 'time'
require 'pp'

FEED_TITLE = "Cheam North and Worcester Park Local Committee"
FEED_IMAGE = "https://dl.dropbox.com/u/300783/sutton-council-logo-1600-sq.jpg"
FEED_AUTHOR = "London Borough of Sutton"
FEED_LINK = "https://www.sutton.gov.uk/index.aspx?articleid=4332"

sourcescraper = 'cheam-north-worcester-park-local-committee-podcast'

ScraperWiki::attach(sourcescraper)

items = ScraperWiki::select("* from swdata order by d desc limit 50")

builder = Nokogiri::XML::Builder.new do |xml|
  xml.rss('xmlns:itunes' => "http://www.itunes.com/dtds/podcast-1.0.dtd", :version => "2.0") {
    xml.channel {
      xml.title FEED_TITLE
      xml.link FEED_LINK
      xml['itunes'].image(:href => FEED_IMAGE)
      xml['itunes'].author FEED_AUTHOR
 
      items.each do |i|
        xml.item {
          xml.title i['title']
          xml['itunes'].author FEED_AUTHOR
          xml.enclosure(:url => i['href'], :type => "audio/mpeg")
          xml.guid i['href']
          xml.pubDate Time.parse(i['d']).rfc822
        }
      end
    }
  }
end

ScraperWiki::httpresponseheader("Content-Type", "application/rss+xml")
puts builder.to_xml