require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new

# Get the AJAX page fragment that contains the odds
page = agent.get 'http://centrebet.com/Sports/2062831'

page.search('table.brdLtGry').each do |table|
  record = {
    party: table.search(:td)[0].inner_text.strip,
    odds: table.search(:td)[1].inner_text.strip,
    date: Date.today
  }

  ScraperWiki.save_sqlite [:party, :date], record
end
require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new

# Get the AJAX page fragment that contains the odds
page = agent.get 'http://centrebet.com/Sports/2062831'

page.search('table.brdLtGry').each do |table|
  record = {
    party: table.search(:td)[0].inner_text.strip,
    odds: table.search(:td)[1].inner_text.strip,
    date: Date.today
  }

  ScraperWiki.save_sqlite [:party, :date], record
end
