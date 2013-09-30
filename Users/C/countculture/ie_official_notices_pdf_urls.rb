# Blank Ruby
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www.irisoifigiuil.ie'

#start_year = 2011

def pdf_refs_from_page(url)
  doc = Nokogiri.HTML(open(url))
  doc.search('#content table tr')[1..-1].collect do |tr|
    tds = tr.search('td')
    edition_number = tds[1].inner_text
    next unless edition_number.strip.match(/^\d+$/)
    {:url => (BASE_URL + tr.at('a')[:href].gsub(' ', '%20')), :edition => tds[1].inner_text, :issue_number => tds[2].inner_text, :created_at => Time.now }
  end.compact
rescue Exception => e
  puts "Exception raised (#{e.inspect}) getting refs from #{url}"
end

#Populate from archive
#current_year = Time.now.year
#(2003..current_year).each do |year|
#  end_month = (year == current_year ?  Time.now.month-1 : 12) # archive contains month prior to current one
#  (1..end_month).each do |month_number|
#    results = pdf_refs_from_page(BASE_URL + "/archive/#{year}/#{Date::MONTHNAMES[month_number].downcase}/")
#    ScraperWiki.save_sqlite([:url], results)
#  end
#end

# Get current issues
results = pdf_refs_from_page('http://www.irisoifigiuil.ie/currentissues/')
ScraperWiki.save_sqlite([:url], results)# Blank Ruby
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www.irisoifigiuil.ie'

#start_year = 2011

def pdf_refs_from_page(url)
  doc = Nokogiri.HTML(open(url))
  doc.search('#content table tr')[1..-1].collect do |tr|
    tds = tr.search('td')
    edition_number = tds[1].inner_text
    next unless edition_number.strip.match(/^\d+$/)
    {:url => (BASE_URL + tr.at('a')[:href].gsub(' ', '%20')), :edition => tds[1].inner_text, :issue_number => tds[2].inner_text, :created_at => Time.now }
  end.compact
rescue Exception => e
  puts "Exception raised (#{e.inspect}) getting refs from #{url}"
end

#Populate from archive
#current_year = Time.now.year
#(2003..current_year).each do |year|
#  end_month = (year == current_year ?  Time.now.month-1 : 12) # archive contains month prior to current one
#  (1..end_month).each do |month_number|
#    results = pdf_refs_from_page(BASE_URL + "/archive/#{year}/#{Date::MONTHNAMES[month_number].downcase}/")
#    ScraperWiki.save_sqlite([:url], results)
#  end
#end

# Get current issues
results = pdf_refs_from_page('http://www.irisoifigiuil.ie/currentissues/')
ScraperWiki.save_sqlite([:url], results)