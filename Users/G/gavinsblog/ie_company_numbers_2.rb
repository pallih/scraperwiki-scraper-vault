require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

page = Nokogiri::HTML(open("http://en.wikipedia.org/"))   
puts page.class   # => Nokogiri::HTML::Document
