# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_party_name_doc(doc)
  result = {}

  table = doc.xpath('id("ContentsBox")/table[1]')[0]

  table.xpath('tr[position() > 1]').each do |tr|
    name, abbr_name = tr.xpath('td').map {|td| td.content }
    result[abbr_name] = name
  end

  result
end

def parse_members_doc(doc, party_name)
  result = []

  table = doc.xpath('id("ContentsBox")/table[2]')[0]

  table.xpath('tr[position() > 1]').each do |tr|
    fields = tr.xpath('td').map do |td|
      td.content.gsub(/(?:\s|\xe3\x80\x80)+/, ' ') # Shrink spaces (\xe3... == full-width space)
    end
    name, furigana, party, district = fields
    real_name = '' 

    if name =~ /\[(.+?)\]/
      real_name = $1
      name.gsub!(/\[.+?\]/, '')
    end

    party.gsub!(/\s/, '')
    party = party_name[party] if party_name.include?(party)

    district.gsub!(/\s/, '')
    
    result << {
      'name'      => name,
      'real_name' => real_name,
      'furigana'  => furigana,
      'party'     => party,
      'district'  => district
    }
  end

  result
end



party_name_url = 'http://www.sangiin.go.jp/japanese/joho1/kousei/giin/kaiha/kaiha177.htm'
members_url = 'http://www.sangiin.go.jp/japanese/joho1/kousei/giin/177/giin.htm'

party_name_doc = Nokogiri::HTML.parse(open(party_name_url), nil, 'UTF-8')
party_name = parse_party_name_doc(party_name_doc)

members_doc = Nokogiri::HTML.parse(open(members_url), nil, 'UTF-8')
data = parse_members_doc(members_doc, party_name)

# (name, furigana) is not unique indeed
ScraperWiki.save(['name', 'furigana'], data)
