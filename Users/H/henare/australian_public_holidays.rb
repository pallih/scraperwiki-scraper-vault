require 'mechanize'
require 'date'

agent = Mechanize.new

page = agent.get 'http://www.fairwork.gov.au/leave/public-holidays/pages/listof2012publicholidays.aspx'

holidays = page.search('.FairWorkTableStyle2TableOddCol').map { |c| Date.parse(c.inner_text) }.uniq.sort

holidays.each do |h|
  ScraperWiki::save_sqlite [:holiday], {holiday: h}
end
require 'mechanize'
require 'date'

agent = Mechanize.new

page = agent.get 'http://www.fairwork.gov.au/leave/public-holidays/pages/listof2012publicholidays.aspx'

holidays = page.search('.FairWorkTableStyle2TableOddCol').map { |c| Date.parse(c.inner_text) }.uniq.sort

holidays.each do |h|
  ScraperWiki::save_sqlite [:holiday], {holiday: h}
end
require 'mechanize'
require 'date'

agent = Mechanize.new

page = agent.get 'http://www.fairwork.gov.au/leave/public-holidays/pages/listof2012publicholidays.aspx'

holidays = page.search('.FairWorkTableStyle2TableOddCol').map { |c| Date.parse(c.inner_text) }.uniq.sort

holidays.each do |h|
  ScraperWiki::save_sqlite [:holiday], {holiday: h}
end
