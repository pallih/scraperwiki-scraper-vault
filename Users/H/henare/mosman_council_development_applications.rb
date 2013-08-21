require 'date'
require 'mechanize'

agent = Mechanize.new
url = "http://portal.mosman.nsw.gov.au/pages/xc.track/RSS.aspx?feed=lodgelast14"

page = Nokogiri::XML(agent.get(url).body)
page.search('item').each do |app|
  record = {
    :address => "#{app.at('title').inner_text.strip}, Mosman, NSW",
    :info_url => app.at('link').inner_text.strip,
    # Giving feedback on the application is on a tab off the application page. Can't seem to link
    # to it directly
    :comment_url => app.at('link').inner_text.strip,
    :description => app.at('description').inner_text.split('</a>- ')[1..-1].join(' - ').split('<br/>')[0].strip,
    :council_reference => Nokogiri.parse(app.at('description').inner_text).inner_text.strip,
    :date_received => app.at('pubDate').inner_text,
    :date_scraped => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
    ScraperWiki.save_sqlite([:council_reference], record)
  else
     puts "Skipping already saved record " + record[:council_reference]
  end
end


require 'date'
require 'mechanize'

agent = Mechanize.new
url = "http://portal.mosman.nsw.gov.au/pages/xc.track/RSS.aspx?feed=lodgelast14"

page = Nokogiri::XML(agent.get(url).body)
page.search('item').each do |app|
  record = {
    :address => "#{app.at('title').inner_text.strip}, Mosman, NSW",
    :info_url => app.at('link').inner_text.strip,
    # Giving feedback on the application is on a tab off the application page. Can't seem to link
    # to it directly
    :comment_url => app.at('link').inner_text.strip,
    :description => app.at('description').inner_text.split('</a>- ')[1..-1].join(' - ').split('<br/>')[0].strip,
    :council_reference => Nokogiri.parse(app.at('description').inner_text).inner_text.strip,
    :date_received => app.at('pubDate').inner_text,
    :date_scraped => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
    ScraperWiki.save_sqlite([:council_reference], record)
  else
     puts "Skipping already saved record " + record[:council_reference]
  end
end


