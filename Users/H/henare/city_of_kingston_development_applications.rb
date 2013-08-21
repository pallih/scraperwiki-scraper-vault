require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new

# Get the last two weeks of data

start_date = (Date.today-14).strftime('%d/%m/%Y')
end_date = Date.today.strftime('%d/%m/%Y')
url = "http://www.kingston.vic.gov.au/web/planning/?l=planning_register2&l1=#{start_date}&l2=#{end_date}&l3=lodged&i=&x=&c=&w="

page = agent.get(url)

page.search('tr.item_row').each do |row|
  values = row.search('td a').map{|a| a.inner_text}
  url = row.at('td a')['href']
  record = {
    'description'       => values[7],
    'council_reference' => values[0],
    'address'           => values[2] + ", " + values[3] + ", VIC",
    'date_received'     => Date.parse(values[1], "%d-%M-&y").to_s,
    'info_url'          => (page.uri + url).to_s,
    'comment_url'       => "http://www.kingston.vic.gov.au/Page/Page.asp?Page_Id=34&h=-1",
    'date_scraped'      => Date.today.to_s,
  }
  # On notice information isn't always there
  if values[4] != ""
    record["on_notice_from"] = Date.parse(values[4], "%d-%M-&y").to_s
  end

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end

require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new

# Get the last two weeks of data

start_date = (Date.today-14).strftime('%d/%m/%Y')
end_date = Date.today.strftime('%d/%m/%Y')
url = "http://www.kingston.vic.gov.au/web/planning/?l=planning_register2&l1=#{start_date}&l2=#{end_date}&l3=lodged&i=&x=&c=&w="

page = agent.get(url)

page.search('tr.item_row').each do |row|
  values = row.search('td a').map{|a| a.inner_text}
  url = row.at('td a')['href']
  record = {
    'description'       => values[7],
    'council_reference' => values[0],
    'address'           => values[2] + ", " + values[3] + ", VIC",
    'date_received'     => Date.parse(values[1], "%d-%M-&y").to_s,
    'info_url'          => (page.uri + url).to_s,
    'comment_url'       => "http://www.kingston.vic.gov.au/Page/Page.asp?Page_Id=34&h=-1",
    'date_scraped'      => Date.today.to_s,
  }
  # On notice information isn't always there
  if values[4] != ""
    record["on_notice_from"] = Date.parse(values[4], "%d-%M-&y").to_s
  end

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end

