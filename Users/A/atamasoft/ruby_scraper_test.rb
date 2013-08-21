# -*- coding: utf-8 -*-
# http://d.hatena.ne.jp/uasi/20110603/1307098299

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

  table = doc.xpath('/html/body')[0]

  # Note tr[1] is actually a table header
  table.xpath('.//table').each do |table|
    fields = table.xpath('.//td').map do |td|
      field = td.text
      field.gsub!(/(?:\s|\xe3\x80\x80)+/, ' ') # Shrink spaces (\xe3... == full-width space)
      field.gsub!(/\s?$/, '')                  # Chop off trailing space
      field
    end
    date, title, place, district, _ = fields
    
    result << {
      'id'     => date,
      'date' => date,
      'title' => title,
     'place'    => place,
#    'district' => district
    }
  end

  result
end



urls = []
urls << "http://www1.plala.or.jp/an/sq/sq/sqq.htm"

urls.each do |url|
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
  data = parse_doc(doc)
  ScraperWiki.save(['id'], data)
end
