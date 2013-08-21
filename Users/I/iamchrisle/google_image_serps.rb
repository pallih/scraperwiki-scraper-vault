require 'nokogiri'
require 'httparty'
require 'pp'

# = GoogleImageSearch
#
# Uses Google Image search to find images simliar to some URL. Scrapes the
# results from Google and returns to you the anchor text, URL, bolded keywords,
# the citation (aka. 'green'), and the snippet.
#
# Author::  Chris Le <chris@iamchrisle.com>
# License:: MIT
#
# === Example
#
#   google_search = GoogleImageSearch.new
#   url = 'http://www.example.com/images/my-image.jpg'
#   serps = google_search.search_by_url(url, 2)
#   puts serps.inspect
#
class GoogleImageSearch
  include HTTParty

  BASE  = "http://images.google.com/searchbyimage?"
  AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.30 '+
          '(KHTML, like Gecko) Chrome/26.0.1403.0 Safari/537.30'

  # Performs a search for similar images by URL
  #
  # Returns an array of hashes.
  #
  # === Arguments
  # +url+::     The URL you want to perform a search for
  # +pages+::   Number of pages you want returned. (default = 1)
  #
  def search_by_url(url, pages = 1)
    serps = []
    url   = URI::encode(url)

    (1..pages).each do |page|
      query = "#{BASE}image_url=#{url}&image_content=&filename=&hl=en"
      start = (page * 10) - 10
      query += "&start=#{start}" if start > 0
      html  = HTTParty.get(query, :headers => { 'User-Agent' => AGENT })
      serps += parse_html_results(html, page)
    end
    serps
  end

  # Returns an array of unique keys returned by the class
  def keys
    [ :anchor_text, :url, :bolded_keywords, :green, :snippet ]
  end

private

  # Collects the SERPs for one page
  #
  # Returns a hash
  #
  # === Arguments
  # +html+::    The body of the Google Page to pull results from
  #
  def parse_html_results(html, page)
    serps = []
    body  = ::Nokogiri::HTML.parse(html)
    n     = 0
    body.search("//div[@class='vsc']").each do |serp|
      serps << {
        :rank            => ((page * 10) - 10 + n + 1),
        :anchor_text     => serp.search('h3/a').text,
        :url             => serp.search('h3/a/@href').text,
        :bolded_keywords => serp.search("em").collect(&:text).uniq,
        :green           => serp.search("cite").text,
        :snippet         => serp.search("span[@class='st']").text.gsub(/\.\.\..*$/,'')
      }
      n += 1
    end
    serps
  end
end

############################################################################
# ScraperWiki test

google_search = GoogleImageSearch.new
url = 'http://upload.wikimedia.org/wikipedia/en/thumb/9/9d/Pepsilogo.png/220px-Pepsilogo.png'
serps = google_search.search_by_url(url, 2)
pp serps.inspect
ScraperWiki::save_sqlite(google_search.keys, serps)
