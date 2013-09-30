require 'nokogiri'
require 'typhoeus'

class ZipCode
  attr_accessor :zip, :city, :state, :county

  def save
    ScraperWiki::save_sqlite(unique_keys=["zip"], data={"zip"=>zip, "city"=>city, "state"=>state, "county" => county})
  end

  def decorate
    "#{city}, #{state} #{zip} (#{county})"
  end
end

BASE_URI = "http://www.quine.org"

def request(endpoint = '/zip-all-00001.html')
  Typhoeus::Request.get "#{BASE_URI}#{endpoint}"
end 

def parse(html)
  Nokogiri::HTML(html)
end

def extract_links(doc)
  doc.xpath("//a[contains(@href, 'zip-all')]/@href").map(&:text)
end

def page_pool
  @pages ||= extract_links(parse(request.body))
end

def normalize(text_line)
  text_line.strip!
  text_line.gsub(/\s\(Corporate Unique - use city name\)/,"")
end

def split_lines(text)
  lines = text.split(/\n/)
  lines.shift
  lines
end

def parse_text(text)
  split_lines(text).map do |line|
    zip_ary = normalize(line).split(', ')
    zip = ZipCode.new
    zip.zip = zip_ary[0]
    zip.city = zip_ary[1]
    zip.state = zip_ary[2]
    zip.county = zip_ary[3]
    puts zip.decorate
    zip.save
  end
end

page_pool.each do |page|
  doc = parse(request("/#{page}").body)
  zip_text = doc.at_xpath('//td[@valign="top"][2]/p').text
  parse_text(zip_text)
end

require 'nokogiri'
require 'typhoeus'

class ZipCode
  attr_accessor :zip, :city, :state, :county

  def save
    ScraperWiki::save_sqlite(unique_keys=["zip"], data={"zip"=>zip, "city"=>city, "state"=>state, "county" => county})
  end

  def decorate
    "#{city}, #{state} #{zip} (#{county})"
  end
end

BASE_URI = "http://www.quine.org"

def request(endpoint = '/zip-all-00001.html')
  Typhoeus::Request.get "#{BASE_URI}#{endpoint}"
end 

def parse(html)
  Nokogiri::HTML(html)
end

def extract_links(doc)
  doc.xpath("//a[contains(@href, 'zip-all')]/@href").map(&:text)
end

def page_pool
  @pages ||= extract_links(parse(request.body))
end

def normalize(text_line)
  text_line.strip!
  text_line.gsub(/\s\(Corporate Unique - use city name\)/,"")
end

def split_lines(text)
  lines = text.split(/\n/)
  lines.shift
  lines
end

def parse_text(text)
  split_lines(text).map do |line|
    zip_ary = normalize(line).split(', ')
    zip = ZipCode.new
    zip.zip = zip_ary[0]
    zip.city = zip_ary[1]
    zip.state = zip_ary[2]
    zip.county = zip_ary[3]
    puts zip.decorate
    zip.save
  end
end

page_pool.each do |page|
  doc = parse(request("/#{page}").body)
  zip_text = doc.at_xpath('//td[@valign="top"][2]/p').text
  parse_text(zip_text)
end

