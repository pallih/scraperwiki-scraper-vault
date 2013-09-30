
results = []
require 'nokogiri'
html = ScraperWiki.scrape("http://clerk.house.gov/member_info/vacancies.aspx")
doc = Nokogiri::HTML(html)
tables = (doc/:table)
tables.each do |table|
  (table/:tr)[1..-1].each do |row|
    d, text = row.children.map{|c| c.text.strip}.reject{|r| r==''}
    state, district = d.split(', ')
    puts text
  end
end
#ScraperWiki.save_sqlite(['person', 'url', 'date'], results)

results = []
require 'nokogiri'
html = ScraperWiki.scrape("http://clerk.house.gov/member_info/vacancies.aspx")
doc = Nokogiri::HTML(html)
tables = (doc/:table)
tables.each do |table|
  (table/:tr)[1..-1].each do |row|
    d, text = row.children.map{|c| c.text.strip}.reject{|r| r==''}
    state, district = d.split(', ')
    puts text
  end
end
#ScraperWiki.save_sqlite(['person', 'url', 'date'], results)
