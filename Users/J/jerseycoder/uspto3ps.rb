# Blank Ruby
require 'mechanize'
require 'net/http'
require 'open-uri'
require 'csv'
require 'highline/import'

ag = Mechanize.new
baseurl = "http://appft1.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=0&f=S&l=50&d=PG01&"
# figure out what today is, then what day the last thursday was.. wday for thursday = 4
today = Date.today 
if today.wday < 5
  lthurs = today - (today.wday + 3)
else
  lthurs = today - (today.wday - 4)
end
dsearch = lthurs.to_s
parts = dsearch.split('-')
# This will search for apps published on the last thursday (patent apps are published every Thurs)
dateq = "Query=PD%2F" + parts[1] + "%2F" + parts[2] + "%2F" + parts[0]
page = ag.get(baseurl + dateq)
listing = page.parser.xpath("//table")
trs = listing[0].xpath("//tr")
trs.each do |tr|
  tds = tr.search('td')
  if tds[0].text == ''
  else
    link = tds[1].search('a')
    link = "http://appft1.uspto.gov" + link.xpath("@href").to_s
    ScraperWiki.save_sqlite(unique_keys=['App No', 'Title', 'Link'], data={"App No" => tds[1].text, "Title" => tds[2].text, "Link" => link} , table_name="PTOApps")
  end
end

#rc_code = page.parser.xpath("//input[@id='recaptcha_response_field']")







# Blank Ruby
require 'mechanize'
require 'net/http'
require 'open-uri'
require 'csv'
require 'highline/import'

ag = Mechanize.new
baseurl = "http://appft1.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=0&f=S&l=50&d=PG01&"
# figure out what today is, then what day the last thursday was.. wday for thursday = 4
today = Date.today 
if today.wday < 5
  lthurs = today - (today.wday + 3)
else
  lthurs = today - (today.wday - 4)
end
dsearch = lthurs.to_s
parts = dsearch.split('-')
# This will search for apps published on the last thursday (patent apps are published every Thurs)
dateq = "Query=PD%2F" + parts[1] + "%2F" + parts[2] + "%2F" + parts[0]
page = ag.get(baseurl + dateq)
listing = page.parser.xpath("//table")
trs = listing[0].xpath("//tr")
trs.each do |tr|
  tds = tr.search('td')
  if tds[0].text == ''
  else
    link = tds[1].search('a')
    link = "http://appft1.uspto.gov" + link.xpath("@href").to_s
    ScraperWiki.save_sqlite(unique_keys=['App No', 'Title', 'Link'], data={"App No" => tds[1].text, "Title" => tds[2].text, "Link" => link} , table_name="PTOApps")
  end
end

#rc_code = page.parser.xpath("//input[@id='recaptcha_response_field']")







