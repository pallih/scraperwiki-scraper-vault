# encoding: utf-8

require 'nokogiri'
require 'open-uri'
require 'json'
require 'uri'

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS rss_feeds (parliamentarian string, blog string, feed_name string, feed string)")

ScraperWiki::attach("finnish_parliamentarians_blogs", "src")           
ScraperWiki::select("* from src.blogs").each do |member|
  JSON.parse(member["blogs"]).each do |blog|
    blog_uri = URI(blog)
    data = Hash["parliamentarian" => member['name'], "blog" => blog]

    begin
      page = Nokogiri::HTML(open(blog_uri.to_s))

      page.css('head link[type="application/rss+xml"]').each do |feed_tag|
        feed_uri = URI(feed_tag['href'])
        if (feed_uri =~ URI::regexp).nil? # relative url
          feed_uri.scheme = blog_uri.scheme
          feed_uri.host = blog_uri.host
        end
        data["feed_name"] = feed_tag['title']
        data["feed"] = feed_uri.to_s
        ScraperWiki::save_sqlite(['feed'], data, table_name="rss_feeds")
      end
    rescue => e
      case e
      when OpenURI::HTTPError
        puts "error reading " + blog_uri.to_s + " : " + e.message
      end
    end
  end
end
# encoding: utf-8

require 'nokogiri'
require 'open-uri'
require 'json'
require 'uri'

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS rss_feeds (parliamentarian string, blog string, feed_name string, feed string)")

ScraperWiki::attach("finnish_parliamentarians_blogs", "src")           
ScraperWiki::select("* from src.blogs").each do |member|
  JSON.parse(member["blogs"]).each do |blog|
    blog_uri = URI(blog)
    data = Hash["parliamentarian" => member['name'], "blog" => blog]

    begin
      page = Nokogiri::HTML(open(blog_uri.to_s))

      page.css('head link[type="application/rss+xml"]').each do |feed_tag|
        feed_uri = URI(feed_tag['href'])
        if (feed_uri =~ URI::regexp).nil? # relative url
          feed_uri.scheme = blog_uri.scheme
          feed_uri.host = blog_uri.host
        end
        data["feed_name"] = feed_tag['title']
        data["feed"] = feed_uri.to_s
        ScraperWiki::save_sqlite(['feed'], data, table_name="rss_feeds")
      end
    rescue => e
      case e
      when OpenURI::HTTPError
        puts "error reading " + blog_uri.to_s + " : " + e.message
      end
    end
  end
end
