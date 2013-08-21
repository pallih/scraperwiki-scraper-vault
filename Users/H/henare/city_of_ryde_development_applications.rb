require 'rubygems'
require 'mechanize'
require 'date'

url = 'http://www.ryde.nsw.gov.au/Development/Development+Applications/DAs+on+Exhibition/Received+Development+Applications'
agent = Mechanize.new

page = agent.get(url)

page.at('div.content-spacing').search('p').each do |p|
  # Skip if this isn't a DA
  next if p.search('strong').count < 3
  
  record = {
    'council_reference' => p.search('strong')[1].next.inner_text.gsub(': ', '').gsub('. ', '').strip,
    'description'       => p.search('strong')[2].next.next.next.inner_text.strip,
    'address'           => p.search('strong')[0].next.inner_text.gsub(': ', '').strip,
    'info_url'          => url,
    'comment_url'       => url,
    'date_scraped'      => Date.today.to_s
  }
  
  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
     puts "Skipping already saved record " + record['council_reference']
  end
end
require 'rubygems'
require 'mechanize'
require 'date'

url = 'http://www.ryde.nsw.gov.au/Development/Development+Applications/DAs+on+Exhibition/Received+Development+Applications'
agent = Mechanize.new

page = agent.get(url)

page.at('div.content-spacing').search('p').each do |p|
  # Skip if this isn't a DA
  next if p.search('strong').count < 3
  
  record = {
    'council_reference' => p.search('strong')[1].next.inner_text.gsub(': ', '').gsub('. ', '').strip,
    'description'       => p.search('strong')[2].next.next.next.inner_text.strip,
    'address'           => p.search('strong')[0].next.inner_text.gsub(': ', '').strip,
    'info_url'          => url,
    'comment_url'       => url,
    'date_scraped'      => Date.today.to_s
  }
  
  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
     puts "Skipping already saved record " + record['council_reference']
  end
end
