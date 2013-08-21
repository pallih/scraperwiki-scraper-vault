# Blank Ruby
require 'rubygems'
require 'mechanize'
require 'morph'

class Crawler
  def initialize(*args)
    args.each {|a| puts a} unless args.empty? 
  end
end
pp ScraperWiki.show_tables()
