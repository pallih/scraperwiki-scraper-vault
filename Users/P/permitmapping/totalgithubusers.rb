# Blank Ruby

require 'nokogiri'
require 'open-uri'

# do as I say and not as I do...
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

doc = Nokogiri::HTML.parse(open('https://github.com/about/press'))
users,repos = doc.css("p > strong").collect {|x| x.text.gsub(',','').to_i}

ScraperWiki::save_sqlite(unique_keys=["date"], data={"date" => Time.now.to_date, "total_github_users"=> users, "total_github_repos"=> repos})
