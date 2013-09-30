#
# Scrapes a list of DL courses from University of Leicester
# Author: Craig Russell <craig@craig-russell.co.uk>
#

require 'digest/sha1'
require 'nokogiri'
require 'set'

html = ScraperWiki::scrape 'http://www2.le.ac.uk/study/ways/distance'
rows = Nokogiri::HTML(html).xpath('//table[@class="data"]//tr')

data = {}

rows.each do |row|
  # Build course
  @title = row.at_xpath('td[1]//a/text()').to_s.strip

  # Messy URLs
  url = row.at_xpath('td[1]//a/@href').to_s.strip
  url.gsub!('../..','')
  @url = 'http://www2.le.ac.uk'+url if url =~ /^\//
  @url = url                        if url =~ /^http/

  # Messy start dates
  a = row.at_xpath('td[2]/p/text()').to_s.split('/').map{|e| e.strip }.to_set
  b = row.at_xpath('td[2]/text()').to_s.split('/').map{|e| e.strip }.to_set
  @start_dates = (a.empty?) ? b : a

  # Messy levels
  a = row.at_xpath('td[1]/p/text()').to_s.gsub('&#160;','').split('/').map{|e| e.strip }.to_set
  b = row.at_xpath('td[1]/text()').to_s.gsub('&#160;','').split('/').map{|e| e.strip }.to_set
  @level = (a.empty?) ? b : a
  
  # Build Course merge with known records using URL as UID
  unless @title.empty? 
    course = data[@url] || {}

    course[:title]= @title unless course[:title]
    course[:url]  = @url   unless course[:url]

    course[:start_dates] = course[:start_dates] || ""
    course[:start_dates] = course[:start_dates].split('/').to_set
    course[:start_dates] << @start_dates
    course[:start_dates] = course[:start_dates].flatten.to_a.join('/')

    course[:level] = course[:level] || ""
    course[:level] = course[:level].split('/').to_set
    course[:level] << @level
    course[:level] = course[:level].flatten.to_a.join('/')

    data[@url] = course
  end
end

# Save courses to DB
data.each_pair do |key, course|
  puts course
  ScraperWiki::save_sqlite(unique_keys=[:url], data=course)
end
#
# Scrapes a list of DL courses from University of Leicester
# Author: Craig Russell <craig@craig-russell.co.uk>
#

require 'digest/sha1'
require 'nokogiri'
require 'set'

html = ScraperWiki::scrape 'http://www2.le.ac.uk/study/ways/distance'
rows = Nokogiri::HTML(html).xpath('//table[@class="data"]//tr')

data = {}

rows.each do |row|
  # Build course
  @title = row.at_xpath('td[1]//a/text()').to_s.strip

  # Messy URLs
  url = row.at_xpath('td[1]//a/@href').to_s.strip
  url.gsub!('../..','')
  @url = 'http://www2.le.ac.uk'+url if url =~ /^\//
  @url = url                        if url =~ /^http/

  # Messy start dates
  a = row.at_xpath('td[2]/p/text()').to_s.split('/').map{|e| e.strip }.to_set
  b = row.at_xpath('td[2]/text()').to_s.split('/').map{|e| e.strip }.to_set
  @start_dates = (a.empty?) ? b : a

  # Messy levels
  a = row.at_xpath('td[1]/p/text()').to_s.gsub('&#160;','').split('/').map{|e| e.strip }.to_set
  b = row.at_xpath('td[1]/text()').to_s.gsub('&#160;','').split('/').map{|e| e.strip }.to_set
  @level = (a.empty?) ? b : a
  
  # Build Course merge with known records using URL as UID
  unless @title.empty? 
    course = data[@url] || {}

    course[:title]= @title unless course[:title]
    course[:url]  = @url   unless course[:url]

    course[:start_dates] = course[:start_dates] || ""
    course[:start_dates] = course[:start_dates].split('/').to_set
    course[:start_dates] << @start_dates
    course[:start_dates] = course[:start_dates].flatten.to_a.join('/')

    course[:level] = course[:level] || ""
    course[:level] = course[:level].split('/').to_set
    course[:level] << @level
    course[:level] = course[:level].flatten.to_a.join('/')

    data[@url] = course
  end
end

# Save courses to DB
data.each_pair do |key, course|
  puts course
  ScraperWiki::save_sqlite(unique_keys=[:url], data=course)
end
