require 'mechanize'
require 'date'

agent = Mechanize.new
url = "http://www.muswellbrook.nsw.gov.au/Council-services/Planning-development/Index-DA.php"

page = agent.get(url)

form = page.forms[1]

form["status"] = 1
page = form.submit

page.search('table.mcs').each do |t|
  t.search('tr').each do |r|
    next if r.at('th') || r.at('td').nil? 

    record = {
      :council_reference => r.search('td')[0].inner_text.strip,
      :address => r.search('td')[1].inner_html.split('<br>')[0].strip,
      :description => r.search('td')[2].inner_text,
      :date_scraped => Date.today.to_s,
      :info_url => url,
      :comment_url => 'mailto:council@muswellbrook.nsw.gov.au'
    }
    status_text = r.search('td')[3].inner_text.strip
    if status_text =~ /Exhibiting\s+until:\s+(.*)/
      record["on_notice_to"] = Date.parse($~[1]).to_s
    end

    if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
      ScraperWiki.save_sqlite([:council_reference], record)
    else
      puts "Skipping already saved record " + record[:council_reference]
    end
  end
end
require 'mechanize'
require 'date'

agent = Mechanize.new
url = "http://www.muswellbrook.nsw.gov.au/Council-services/Planning-development/Index-DA.php"

page = agent.get(url)

form = page.forms[1]

form["status"] = 1
page = form.submit

page.search('table.mcs').each do |t|
  t.search('tr').each do |r|
    next if r.at('th') || r.at('td').nil? 

    record = {
      :council_reference => r.search('td')[0].inner_text.strip,
      :address => r.search('td')[1].inner_html.split('<br>')[0].strip,
      :description => r.search('td')[2].inner_text,
      :date_scraped => Date.today.to_s,
      :info_url => url,
      :comment_url => 'mailto:council@muswellbrook.nsw.gov.au'
    }
    status_text = r.search('td')[3].inner_text.strip
    if status_text =~ /Exhibiting\s+until:\s+(.*)/
      record["on_notice_to"] = Date.parse($~[1]).to_s
    end

    if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
      ScraperWiki.save_sqlite([:council_reference], record)
    else
      puts "Skipping already saved record " + record[:council_reference]
    end
  end
end
require 'mechanize'
require 'date'

agent = Mechanize.new
url = "http://www.muswellbrook.nsw.gov.au/Council-services/Planning-development/Index-DA.php"

page = agent.get(url)

form = page.forms[1]

form["status"] = 1
page = form.submit

page.search('table.mcs').each do |t|
  t.search('tr').each do |r|
    next if r.at('th') || r.at('td').nil? 

    record = {
      :council_reference => r.search('td')[0].inner_text.strip,
      :address => r.search('td')[1].inner_html.split('<br>')[0].strip,
      :description => r.search('td')[2].inner_text,
      :date_scraped => Date.today.to_s,
      :info_url => url,
      :comment_url => 'mailto:council@muswellbrook.nsw.gov.au'
    }
    status_text = r.search('td')[3].inner_text.strip
    if status_text =~ /Exhibiting\s+until:\s+(.*)/
      record["on_notice_to"] = Date.parse($~[1]).to_s
    end

    if ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? 
      ScraperWiki.save_sqlite([:council_reference], record)
    else
      puts "Skipping already saved record " + record[:council_reference]
    end
  end
end
