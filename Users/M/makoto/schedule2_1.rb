# Blank Ruby

# -*- coding: utf-8 -*-
require 'rubygems'
require 'open-uri'
require 'nokogiri'
require "net/http"
require "uri"
require 'csv'
# require 'activerecord'
# ActiveRecord::Base.establish_connection(:adapter => 'sqlite3', :database => 'data/bbc/bbc_schedule.sqlite



def get_doc(url_text)
  url = URI.parse(url_text)
  p url
  req = Net::HTTP::Get.new(url_text)

  puts "Fetching #{url_text}"

  res = Net::HTTP.new(url.host, url.port).start do |http|
    http.request(req)
  end

  res.body
end

def get_file(file_name)
  File.open(file_name).read
end

def run(page)
  results = []
  doc =  Nokogiri::HTML.parse(get_doc(page))
  # p doc
  local_date = page.split('/').last
  
  doc.css('.one-day-all-sports .container').each do |category_elem|
    category = category_elem.css('h2').text.strip
    
    category_elem.css('.session-block').each do |session_elem|

      session_elem.css('h4').each do |time_elem|
        local_time = time_elem.css('.time').text.strip
        date_time_node = time_elem.css('.time').children.css('time')
        # p category
        # p local_time
        date_time = date_time_node.attribute('datetime').value if date_time_node && date_time_node.length > 0
        
        start_time, end_time = local_time.split(" - ")
        start_time_epoch = Time.parse("#{local_date} #{start_time}:00 +0100").to_i
        end_time_epoch   = Time.parse("#{local_date} #{end_time}:00 +0100").to_i
        
        # p start_time_epoch
        # p end_time_epoch
        
        time_elem.next.next.next.next.css('li').each do |detail_elem|
          event = detail_elem.css('.event').text.strip
          phase = detail_elem.css('.phase').text.strip
          medal = detail_elem.css('.medal-event').text.strip
          is_medal = medal == "" ? false : true
          data = {:local_date => local_date, :local_time => local_time, :start_time_epoch => start_time_epoch, :end_time_epoch => end_time_epoch, :category => category, :medal => is_medal, :event => event, :phase => phase}
          row = [local_date, local_time, start_time_epoch, end_time_epoch, category, is_medal, event, phase]
          results << row
          ScraperWiki::save_sqlite(unique_keys=[:local_date, :local_time, :category, :event], data=data)
        end
      end
    end
  end
  results
end

results = []

(25..31).to_a.each do |d|
  p "./data/bbc/201207#{d}"
  url = "http://www.bbc.co.uk/sport/olympics/2012/schedule-results/list/201207#{d}"
  p url
  rows = run(url)
  rows.each{|r| results.push r}
end

(1..9).to_a.each do |d|
  url = "http://www.bbc.co.uk/sport/olympics/2012/schedule-results/list/2012080#{d}"
  rows = run(url)
  rows.each{|r| results.push r}
end

(10..12).to_a.each do |d|
  url = "http://www.bbc.co.uk/sport/olympics/2012/schedule-results/list/201208#{d}"
  rows = run(url)
  rows.each{|r| results.push r}
end
# Blank Ruby

# -*- coding: utf-8 -*-
require 'rubygems'
require 'open-uri'
require 'nokogiri'
require "net/http"
require "uri"
require 'csv'
# require 'activerecord'
# ActiveRecord::Base.establish_connection(:adapter => 'sqlite3', :database => 'data/bbc/bbc_schedule.sqlite



def get_doc(url_text)
  url = URI.parse(url_text)
  p url
  req = Net::HTTP::Get.new(url_text)

  puts "Fetching #{url_text}"

  res = Net::HTTP.new(url.host, url.port).start do |http|
    http.request(req)
  end

  res.body
end

def get_file(file_name)
  File.open(file_name).read
end

def run(page)
  results = []
  doc =  Nokogiri::HTML.parse(get_doc(page))
  # p doc
  local_date = page.split('/').last
  
  doc.css('.one-day-all-sports .container').each do |category_elem|
    category = category_elem.css('h2').text.strip
    
    category_elem.css('.session-block').each do |session_elem|

      session_elem.css('h4').each do |time_elem|
        local_time = time_elem.css('.time').text.strip
        date_time_node = time_elem.css('.time').children.css('time')
        # p category
        # p local_time
        date_time = date_time_node.attribute('datetime').value if date_time_node && date_time_node.length > 0
        
        start_time, end_time = local_time.split(" - ")
        start_time_epoch = Time.parse("#{local_date} #{start_time}:00 +0100").to_i
        end_time_epoch   = Time.parse("#{local_date} #{end_time}:00 +0100").to_i
        
        # p start_time_epoch
        # p end_time_epoch
        
        time_elem.next.next.next.next.css('li').each do |detail_elem|
          event = detail_elem.css('.event').text.strip
          phase = detail_elem.css('.phase').text.strip
          medal = detail_elem.css('.medal-event').text.strip
          is_medal = medal == "" ? false : true
          data = {:local_date => local_date, :local_time => local_time, :start_time_epoch => start_time_epoch, :end_time_epoch => end_time_epoch, :category => category, :medal => is_medal, :event => event, :phase => phase}
          row = [local_date, local_time, start_time_epoch, end_time_epoch, category, is_medal, event, phase]
          results << row
          ScraperWiki::save_sqlite(unique_keys=[:local_date, :local_time, :category, :event], data=data)
        end
      end
    end
  end
  results
end

results = []

(25..31).to_a.each do |d|
  p "./data/bbc/201207#{d}"
  url = "http://www.bbc.co.uk/sport/olympics/2012/schedule-results/list/201207#{d}"
  p url
  rows = run(url)
  rows.each{|r| results.push r}
end

(1..9).to_a.each do |d|
  url = "http://www.bbc.co.uk/sport/olympics/2012/schedule-results/list/2012080#{d}"
  rows = run(url)
  rows.each{|r| results.push r}
end

(10..12).to_a.each do |d|
  url = "http://www.bbc.co.uk/sport/olympics/2012/schedule-results/list/201208#{d}"
  rows = run(url)
  rows.each{|r| results.push r}
end
