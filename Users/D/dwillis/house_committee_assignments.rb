require 'open-uri'
require 'nokogiri'
require 'date'
require 'json'

# encoding: UTF-8
# Scraper for House Clerk's list of Committee and Subcommittee Assignments
# This saves membership for committees and subcommittees based on the date the
# scraper is run, meaning that it will produce a new version of each committee
# for each date, in order to make it possible to see a history of a committee's
# membership.

# can't use ScraperWiki.scrape because there's Unicode hiding amidst the ASCII!

# get committee urls
html = open("http://clerk.house.gov/committee_info/index.aspx").read
doc = Nokogiri::HTML(html.encode('UTF-8'))

# build array of committees
comms = []
url_list = (doc/:ul)[2]
(url_list/:a).each do |link|
  code = link['href'].split('=').last
  comms << {'code' => code, 'name' => link.text, 'url' => 'http://clerk.house.gov' + link['href'], 'date' => Date.today}
end

# loop through array of committees, populating majority and minority membership and identifying chairmen and ranking members.
comms.each do |comm|
  html = open(comm['url']).read
  doc = Nokogiri::HTML(html.encode('UTF-8'))
  majority_members = doc.xpath('//div[@id="primary_group"]/ol/li/a').map{|m| Hash['state', m['href'].split('=').last[0..1], 'district',m['href'].split('=').last[2..-1], 'name', m.text.strip]}
  majority_members.first['chairman'] = true
  minority_members = doc.xpath('//div[@id="secondary_group"]/ol/li/a').map{|m| {'state' => m['href'].split('=').last[0..1], 'district' => m['href'].split('=').last[2..-1], 'name' => m.text.strip}}
  minority_members.first['ranking_member'] = true
  comm['majority_members'] = majority_members.to_json
  comm['minority_members'] = minority_members.to_json
  # identify subcommittees and loop through them, populating majority & minority membership
  subcoms = doc.xpath('//div[@id="subcom_list"]/ul/li/a')
  subcommittees = subcoms.map{|s| {'code' => s['href'].split('=').last, 'name' => s.text.strip, 'url' => 'http://clerk.house.gov'+s['href']}}
  subcommittees.each do |subcommittee|
    html = open(subcommittee['url']).read
    doc = Nokogiri::HTML(html.encode('UTF-8'))
    majority_members = doc.xpath('//div[@id="primary_group"]/ol/li/a').map{|m| {'state' => m['href'].split('=').last[0..1], 'district' => m['href'].split('=').last[2..-1], 'name' => m.text.strip}}
    majority_members.first['chairman'] = true
    minority_members = doc.xpath('//div[@id="secondary_group"]/ol/li/a').map{|m| {'state' => m['href'].split('=').last[0..1], 'district' => m['href'].split('=').last[2..-1], 'name' => m.text.strip}}
    minority_members.first['ranking_member'] = true
    subcommittee['majority_members'] = majority_members.to_json
    subcommittee['minority_members'] = minority_members.to_json
  end
  # add subcommittees to committee object
  comm['subcommittees'] = subcommittees.to_json
end
ScraperWiki.save_sqlite(["code", "date"], comms)
