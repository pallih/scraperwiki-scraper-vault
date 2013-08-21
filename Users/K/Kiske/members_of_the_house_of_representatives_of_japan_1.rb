# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

  table = doc.xpath('/html/body/table[2]//table')[0]

  # Note tr[1] is actually a table header
  table.xpath('tr[position() > 1]').each do |tr|
    fields = tr.xpath('td').map do |td|
      field = td.content
      field.gsub!(/(?:\s|\xe3\x80\x80)+/, ' ') # Shrink spaces (\xe3... == full-width space)
      field.gsub!(/\s?$/, '')                  # Chop off trailing space
      field
    end
    name, furigana, party, district, _ = fields
    
    name.gsub!(/.$/, '') # Chop off "-kun"

    result << {
      'name'     => name,
      'furigana' => furigana,
      'party'    => party,
      'district' => district
    }
  end

  result
end



urls = (1..10).map {|i| "http://www.shugiin.go.jp/itdb_annai.nsf/html/statics/syu/#{i}giin.htm" }

urls.each do |url|
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url))
  data = parse_doc(doc)
  # (name, furigana) is not unique indeed
  ScraperWiki.save(['name', 'furigana'], data)
end
