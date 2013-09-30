# -*- coding: utf-8 -*-
 
require 'rubygems'
require 'mechanize'
require 'open-uri'
require 'nokogiri'

agent = Mechanize.new

for i in 1..5
  agent.get("http://www2s.biglobe.ne.jp/~fufufu/ekidata/search.cgi?PREF=all&EMAIL=all&FF=#{i}")
  names = agent.page.root.search('table>tr')

  names.each do |n|
    l = n.search('td')
    if l[0] and l[2] and l[6]
      ScraperWiki.save_sqlite(unique_keys=['name'],data={'name'=>l[0].inner_text, 'addr'=>l[2].inner_text, 'kana'=>l[6].inner_text})
    end
  end
end


# -*- coding: utf-8 -*-
 
require 'rubygems'
require 'mechanize'
require 'open-uri'
require 'nokogiri'

agent = Mechanize.new

for i in 1..5
  agent.get("http://www2s.biglobe.ne.jp/~fufufu/ekidata/search.cgi?PREF=all&EMAIL=all&FF=#{i}")
  names = agent.page.root.search('table>tr')

  names.each do |n|
    l = n.search('td')
    if l[0] and l[2] and l[6]
      ScraperWiki.save_sqlite(unique_keys=['name'],data={'name'=>l[0].inner_text, 'addr'=>l[2].inner_text, 'kana'=>l[6].inner_text})
    end
  end
end


