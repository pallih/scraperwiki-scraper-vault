# -*- encoding: utf-8 -*-
%w|rubygems mechanize open-uri|.each{|x| require x}

target = "http://ja.wikipedia.org/wiki/%E3%83%AB%E3%83%BC%E3%83%97%E3%82%82%E3%81%AE"

# scrape
doc = Mechanize.new{|a|a.user_agent_alias = "Windows Mozilla"}.get(target)
# get stories only
stories = doc.search('#bodyContent .mw-content-ltr').text.scan(/『(.+?)』/).map(&:first).uniq

# save to DB
ScraperWiki.save_sqlite(unique_keys=[:name], stories.map{|x| {:name => x} })

puts stories# -*- encoding: utf-8 -*-
%w|rubygems mechanize open-uri|.each{|x| require x}

target = "http://ja.wikipedia.org/wiki/%E3%83%AB%E3%83%BC%E3%83%97%E3%82%82%E3%81%AE"

# scrape
doc = Mechanize.new{|a|a.user_agent_alias = "Windows Mozilla"}.get(target)
# get stories only
stories = doc.search('#bodyContent .mw-content-ltr').text.scan(/『(.+?)』/).map(&:first).uniq

# save to DB
ScraperWiki.save_sqlite(unique_keys=[:name], stories.map{|x| {:name => x} })

puts stories