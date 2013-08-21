require 'mechanize'
require 'date'

url = 'http://www.charterstowers.qld.gov.au/web/guest/planning-and-development-services'
agent = Mechanize.new

page = agent.get url

table = page.search(:table).last

table.search(:tr).each_with_index do |row,number|
  next if number == 0 # Skip header

  columns = row.search(:td)

  record = {
    council_reference: columns[0].inner_text,
    date_received:     Date.strptime(columns[1].inner_text, '%d/%m/%Y'),
    description:       columns[3].inner_text,
    address:           "#{columns[4].inner_text}, QLD",
    info_url:          url,
    comment_url:       'mailto:mail@charterstowers.qld.gov.au', 
    date_scraped:      Date.today
  }

  if (ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? rescue true)
    ScraperWiki.save_sqlite([:council_reference], record)
  else
    puts "Skipping already saved record " + record[:council_reference]
  end
end
