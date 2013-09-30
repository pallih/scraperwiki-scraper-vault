require 'mechanize'
require 'nokogiri'
require 'yaml'
require 'open-uri'
require 'json'

url = 'http://oneinthejungle.com'

agent = Mechanize.new
  
page = agent.get(url)
  
doc = Nokogiri.HTML(page.content)

table = doc.search('table')[0]

table.search('tr').each do |row|
  if row.search('td').length > 2
    details = {}
    details[:show] = row.search('td')[1].inner_text
    details[:link] = url + row.search('td')[1].search('a')[0][:href] rescue nil
    details[:link2] = url + row.search('td')[1].search('a')[1][:href] rescue nil
    details[:link3] = url + row.search('td')[1].search('a')[2][:href] rescue nil
    details[:date] = row.search('td')[0].inner_text
    details[:length] = row.search('td')[2].inner_text

    ScraperWiki.save([:date], details)
  end
endrequire 'mechanize'
require 'nokogiri'
require 'yaml'
require 'open-uri'
require 'json'

url = 'http://oneinthejungle.com'

agent = Mechanize.new
  
page = agent.get(url)
  
doc = Nokogiri.HTML(page.content)

table = doc.search('table')[0]

table.search('tr').each do |row|
  if row.search('td').length > 2
    details = {}
    details[:show] = row.search('td')[1].inner_text
    details[:link] = url + row.search('td')[1].search('a')[0][:href] rescue nil
    details[:link2] = url + row.search('td')[1].search('a')[1][:href] rescue nil
    details[:link3] = url + row.search('td')[1].search('a')[2][:href] rescue nil
    details[:date] = row.search('td')[0].inner_text
    details[:length] = row.search('td')[2].inner_text

    ScraperWiki.save([:date], details)
  end
end