require 'mechanize'

url = 'http://ecouncil.lanecove.nsw.gov.au/trim/advertisedDAs.aspx'
comment_url = 'mailto:lccouncil@lanecove.nsw.gov.au'
agent = Mechanize.new

doc = agent.get url

# Process results table - doesn't seem to be paginated
# Each section lacks a container, so process each element in the overall container
# Keeps track of the suburb from the H4's, then grabs the rest from the following TABLE
fullcontent = doc.at('#fullcontent')
if not fullcontent.nil? and not fullcontent.search('div')[5].nil? 
  address = ""
  fullcontent.search('div')[5].children.each do |block|
    case block.name
    when "text", "comment", "script", "p"
      # Do nothing
    when "h4"
      @suburb = block.inner_text.strip
    when "table"
      application_dates = block.search('tr')[4].search('td')[2].inner_text.strip.split('Expiry: ')

      record = {
        'info_url' => block.search('tr')[3].search('td')[2].at('a').attr('href'),
        'comment_url' => comment_url,
        'council_reference' => block.search('tr')[3].search('td')[2].inner_text.strip,
        'on_notice_from' => Date.strptime(application_dates[0], '%d/%m/%Y').to_s,
        'on_notice_to' => Date.strptime(application_dates[1], '%d/%m/%Y').to_s,
        'address' => "#{block.search('tr')[0].at('td').inner_text.strip}, #{@suburb}",
        'description' => block.search('tr')[1].search('td')[2].inner_text.strip,
        'date_scraped' => Date.today.to_s
      }
        
      #p record
      if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
        puts "Saving new record " + record['council_reference']
        ScraperWiki.save_sqlite(['council_reference'], record)
      else
        puts "Skipping already saved record " + record['council_reference']
      end
    else
      raise "Unexpected type: #{block.name} #{block}"
    end
  end
end

require 'mechanize'

url = 'http://ecouncil.lanecove.nsw.gov.au/trim/advertisedDAs.aspx'
comment_url = 'mailto:lccouncil@lanecove.nsw.gov.au'
agent = Mechanize.new

doc = agent.get url

# Process results table - doesn't seem to be paginated
# Each section lacks a container, so process each element in the overall container
# Keeps track of the suburb from the H4's, then grabs the rest from the following TABLE
fullcontent = doc.at('#fullcontent')
if not fullcontent.nil? and not fullcontent.search('div')[5].nil? 
  address = ""
  fullcontent.search('div')[5].children.each do |block|
    case block.name
    when "text", "comment", "script", "p"
      # Do nothing
    when "h4"
      @suburb = block.inner_text.strip
    when "table"
      application_dates = block.search('tr')[4].search('td')[2].inner_text.strip.split('Expiry: ')

      record = {
        'info_url' => block.search('tr')[3].search('td')[2].at('a').attr('href'),
        'comment_url' => comment_url,
        'council_reference' => block.search('tr')[3].search('td')[2].inner_text.strip,
        'on_notice_from' => Date.strptime(application_dates[0], '%d/%m/%Y').to_s,
        'on_notice_to' => Date.strptime(application_dates[1], '%d/%m/%Y').to_s,
        'address' => "#{block.search('tr')[0].at('td').inner_text.strip}, #{@suburb}",
        'description' => block.search('tr')[1].search('td')[2].inner_text.strip,
        'date_scraped' => Date.today.to_s
      }
        
      #p record
      if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
        puts "Saving new record " + record['council_reference']
        ScraperWiki.save_sqlite(['council_reference'], record)
      else
        puts "Skipping already saved record " + record['council_reference']
      end
    else
      raise "Unexpected type: #{block.name} #{block}"
    end
  end
end

