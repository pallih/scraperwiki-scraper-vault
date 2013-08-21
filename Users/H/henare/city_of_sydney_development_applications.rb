require 'rss/2.0'
require 'date'

feed = RSS::Parser.parse("http://feeds.cityofsydney.nsw.gov.au/SydneyDAs", false)

feed.channel.items.each do |item|
  record = {
    "address" => item.title.gsub(' *NEW*',''),
    "description" => item.description.split('p>')[3].gsub('</',''),
    "date_received" => item.pubDate.strftime('%Y-%m-%d'),
    "on_notice_to" => Date.parse(item.description.split('Exhibition Closes: </strong>')[1].split('</p>')[0]).strftime('%Y-%m-%d'),
    "council_reference" => item.description.split('DA Number: </strong>')[1].split('<p>')[0],
    "info_url" => item.description.split('<a href="')[1].split('">View')[0],
    "comment_url" => "mailto:dasubmissions@cityofsydney.nsw.gov.au",
    "date_scraped" => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end
require 'rss/2.0'
require 'date'

feed = RSS::Parser.parse("http://feeds.cityofsydney.nsw.gov.au/SydneyDAs", false)

feed.channel.items.each do |item|
  record = {
    "address" => item.title.gsub(' *NEW*',''),
    "description" => item.description.split('p>')[3].gsub('</',''),
    "date_received" => item.pubDate.strftime('%Y-%m-%d'),
    "on_notice_to" => Date.parse(item.description.split('Exhibition Closes: </strong>')[1].split('</p>')[0]).strftime('%Y-%m-%d'),
    "council_reference" => item.description.split('DA Number: </strong>')[1].split('<p>')[0],
    "info_url" => item.description.split('<a href="')[1].split('">View')[0],
    "comment_url" => "mailto:dasubmissions@cityofsydney.nsw.gov.au",
    "date_scraped" => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end
