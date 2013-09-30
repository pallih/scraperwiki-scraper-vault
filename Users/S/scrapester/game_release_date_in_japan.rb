#!/bin/env ruby
# -*- coding: utf-8 -*-

require 'rubygems'
require 'nokogiri'
require 'open-uri'

def detect_platform(uri)
  uri.match(/\/([^.\/]++)\.\w++$/).to_a.last.upcase
end

def sanitize_string(str)
  str.strip.gsub("\u{301c}","\u{ff5e}")
end

uri = 'http://app1.watch.impress.co.jp/shiplist.php?symbol=gmw_ship'
doc = Nokogiri::HTML.parse( open(uri) )
table = doc.xpath('//table[@cellspacing=1][@cellpadding=1][@border=1]').first
result = []
date = nil
table.xpath('tr[position() > 1]').each do |tr|
  if tr.has_attribute?('style')
    date = Date.strptime( tr.at('th').content.strip, '%Y年%m月%d日' )
  else
    cols = tr.xpath('td')
    result << {
      date:     date.strftime("%Y/%m/%d (#{%w(日 月 火 水 木 金 土)[date.wday]})"),
      platform: detect_platform(cols[0].at('img')['src']),
      title:    sanitize_string(cols[1].content),
      maker:    sanitize_string(cols[2].content),
      genre:    sanitize_string(cols[3].content),
      price:    sanitize_string(cols[4].content).delete('円'),
    }
  end
end

ScraperWiki.save([:platform, :title], result)

#!/bin/env ruby
# -*- coding: utf-8 -*-

require 'rubygems'
require 'nokogiri'
require 'open-uri'

def detect_platform(uri)
  uri.match(/\/([^.\/]++)\.\w++$/).to_a.last.upcase
end

def sanitize_string(str)
  str.strip.gsub("\u{301c}","\u{ff5e}")
end

uri = 'http://app1.watch.impress.co.jp/shiplist.php?symbol=gmw_ship'
doc = Nokogiri::HTML.parse( open(uri) )
table = doc.xpath('//table[@cellspacing=1][@cellpadding=1][@border=1]').first
result = []
date = nil
table.xpath('tr[position() > 1]').each do |tr|
  if tr.has_attribute?('style')
    date = Date.strptime( tr.at('th').content.strip, '%Y年%m月%d日' )
  else
    cols = tr.xpath('td')
    result << {
      date:     date.strftime("%Y/%m/%d (#{%w(日 月 火 水 木 金 土)[date.wday]})"),
      platform: detect_platform(cols[0].at('img')['src']),
      title:    sanitize_string(cols[1].content),
      maker:    sanitize_string(cols[2].content),
      genre:    sanitize_string(cols[3].content),
      price:    sanitize_string(cols[4].content).delete('円'),
    }
  end
end

ScraperWiki.save([:platform, :title], result)

