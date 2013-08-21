# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

  table = doc.xpath('/html/body//table')[1]

  # Note tr[1] is actually a table header
  table.xpath('tr[position() > 1]').each do |tr|
    fields = tr.xpath('td').map do |td|
      field = td.text 
      field.gsub!(/(?:\s|\xe3\x80\x80)+/, ' ') # Shrink spaces (\xe3... == full-width space)
      field.gsub!(/\s?$/, '')                  # Chop off trailing space
      field
    end
    name, furigana, party, district, _ = fields
    
    name.gsub!(/\[.*$/, '') # Ignore real name
    puts name
    result << {
      'name'     => name,
      'furigana' => furigana,
      'party'    => party,
      'district' => district
    }
  end

  result
end
  url = "http://www.sangiin.go.jp/japanese/joho1/kousei/giin/179/giin.htm"
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url))
  data = parse_doc(doc)
  ScraperWiki.save(['name', 'furigana'], data)