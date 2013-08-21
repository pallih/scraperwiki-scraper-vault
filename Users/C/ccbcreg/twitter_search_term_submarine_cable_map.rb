require "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_timerequire "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'

def search_terms
  ["Submarine%20Cable%20Map"]
end

def one_stinking_day
  (24*60*60)
end

def date_stamp(d = nil)
  d == 1 ? (Time.now() + one_stinking_day).strftime("%Y-%m-%d") : (Time.now() - one_stinking_day).strftime("%Y-%m-%d")
end

def write(term)
  (1..15).each do |x|
    puts "#{date_stamp()} #{date_stamp(1)}"
    puts "http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}"
    pages = JSON.parse(open("http://search.twitter.com/search.json?q=#{term}&since=#{date_stamp()}&until=#{date_stamp(1)}&rpp=100&page=#{x}") {|f| f.read})
    puts pages.inspect
    pages["results"].each do |r|
      ScraperWiki.save_sqlite(unique_keys=['id'], data=r)
    end if !pages["results"].empty? 
    puts "Page: #{x}"
  end
end

def twitter_time
  search_terms.each do |term|
    write(term)
  end
end

twitter_time