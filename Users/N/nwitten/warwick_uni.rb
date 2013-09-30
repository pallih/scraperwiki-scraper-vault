# Warwick library API v1.0

require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

$BASE_URL = 'http://www2.warwick.ac.uk'
$urls = Array.new

class WarwickScraper

  def initialize()
  
    ScraperWiki.sqliteexecute('CREATE TABLE IF NOT EXISTS `contentmap` (`url`, `name`, `lastmodified`, `parent`)')
    ScraperWiki.sqliteexecute('CREATE TABLE IF NOT EXISTS `content` (`url`, `name`, `content`)')

    url = $BASE_URL + '/services/library/'
    
    a = Mechanize.new
    
    # Fetch the URL
    a.get(url)
    
    doc = Nokogiri.HTML(a.page.body)
    
    # Get top level nav items
    topnav = doc.css('#primary-navigation li')
    
    # Recurse the contentmap from the top
    get_contentmap(topnav, parent=nil)

  end

  
  
  def get_contentmap(basenav, parent)
  
    basenav.each do |nav|
      contentmap = {}
      
      #if nav.search('a').empty? 
        
      #  puts "EMPTY #{parent}"
      #  puts nav
      #  return
      #end 
  
      link = nav.search('a')
      
  
      if !link.empty? && link[0]['href'] != parent
    
        contentmap['lastmodified'] = nav['data-lastmodified']
        contentmap['url'] = nav.search('a')[0]['href']
        contentmap['name'] = nav.search('a div.title')[0].inner_text
        contentmap['parent'] = parent
        
        ScraperWiki::save_sqlite(unique_keys=["url"], data=contentmap, table_name="contentmap")    
    
        
        get_contentpage(contentmap['url'])
      end
    
    end
  
  end
  
  
  def get_contentpage(url)
  
  
    # Check to see if we've already seen this content
    if $urls.include?(url)
      # Already parsed
      return
    end 
    $urls.push(url) 
  
  
    begin
      a = Mechanize.new
      
      # Fetch the URL
      a.get($BASE_URL + url)
    rescue Exception => ex
     puts "Parsing error: #{ex}"
     puts "        URL:   #{url}"
     return
    end 
  
  
    doc = Nokogiri.HTML(a.page.body)
  
    content = {}
    content['url'] = url
    content['name'] = doc.css('#main-content h1')[0].inner_text
    content['content'] = doc.css('#column-1-content')[0].inner_text

    children = doc.css('#secondary-navigation li')
    
    get_contentmap(children, parent = url)
  
  end

end

scraper = WarwickScraper.new()


# Warwick library API v1.0

require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

$BASE_URL = 'http://www2.warwick.ac.uk'
$urls = Array.new

class WarwickScraper

  def initialize()
  
    ScraperWiki.sqliteexecute('CREATE TABLE IF NOT EXISTS `contentmap` (`url`, `name`, `lastmodified`, `parent`)')
    ScraperWiki.sqliteexecute('CREATE TABLE IF NOT EXISTS `content` (`url`, `name`, `content`)')

    url = $BASE_URL + '/services/library/'
    
    a = Mechanize.new
    
    # Fetch the URL
    a.get(url)
    
    doc = Nokogiri.HTML(a.page.body)
    
    # Get top level nav items
    topnav = doc.css('#primary-navigation li')
    
    # Recurse the contentmap from the top
    get_contentmap(topnav, parent=nil)

  end

  
  
  def get_contentmap(basenav, parent)
  
    basenav.each do |nav|
      contentmap = {}
      
      #if nav.search('a').empty? 
        
      #  puts "EMPTY #{parent}"
      #  puts nav
      #  return
      #end 
  
      link = nav.search('a')
      
  
      if !link.empty? && link[0]['href'] != parent
    
        contentmap['lastmodified'] = nav['data-lastmodified']
        contentmap['url'] = nav.search('a')[0]['href']
        contentmap['name'] = nav.search('a div.title')[0].inner_text
        contentmap['parent'] = parent
        
        ScraperWiki::save_sqlite(unique_keys=["url"], data=contentmap, table_name="contentmap")    
    
        
        get_contentpage(contentmap['url'])
      end
    
    end
  
  end
  
  
  def get_contentpage(url)
  
  
    # Check to see if we've already seen this content
    if $urls.include?(url)
      # Already parsed
      return
    end 
    $urls.push(url) 
  
  
    begin
      a = Mechanize.new
      
      # Fetch the URL
      a.get($BASE_URL + url)
    rescue Exception => ex
     puts "Parsing error: #{ex}"
     puts "        URL:   #{url}"
     return
    end 
  
  
    doc = Nokogiri.HTML(a.page.body)
  
    content = {}
    content['url'] = url
    content['name'] = doc.css('#main-content h1')[0].inner_text
    content['content'] = doc.css('#column-1-content')[0].inner_text

    children = doc.css('#secondary-navigation li')
    
    get_contentmap(children, parent = url)
  
  end

end

scraper = WarwickScraper.new()


