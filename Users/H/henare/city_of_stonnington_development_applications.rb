require 'mechanize'

agent = Mechanize.new
url = 'http://www.stonnington.vic.gov.au/PlanningRegister.aspx?PageID=567'

page = agent.get(url)

# Get the last 10 days development application (in case ScraperWiki decides not to run)
form = page.forms.first
form.field_with(:name => 'ctl00$phContent$txtDateFrom').value = (Date.today - 10).strftime("%d/%m/%Y")
form.field_with(:name => 'ctl00$phContent$txtDateTo').value = Date.today.strftime("%d/%m/%Y")
form['ctl00$phContent$ddlResultsPerPage'] = 200
page = form.submit

page.at("table#ctl00_phContent_gvPlanningRegister").search('tr')[1..-1].each do |r|
  record = {
    'info_url' => (page.uri + r.at('a')['href']).to_s,
    'comment_url' => "mailto:council@stonnington.vic.gov.au",
    'council_reference' => r.search('td')[0].inner_text,
    'date_received' => Date.strptime(r.search('td')[1].inner_text.strip, '%d/%m/%Y').to_s,
    'address' => r.search('td')[3].inner_text.strip + ", VIC",
    'description' => r.search('td')[4].inner_text.strip,
    'date_scraped' => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
endrequire 'mechanize'

agent = Mechanize.new
url = 'http://www.stonnington.vic.gov.au/PlanningRegister.aspx?PageID=567'

page = agent.get(url)

# Get the last 10 days development application (in case ScraperWiki decides not to run)
form = page.forms.first
form.field_with(:name => 'ctl00$phContent$txtDateFrom').value = (Date.today - 10).strftime("%d/%m/%Y")
form.field_with(:name => 'ctl00$phContent$txtDateTo').value = Date.today.strftime("%d/%m/%Y")
form['ctl00$phContent$ddlResultsPerPage'] = 200
page = form.submit

page.at("table#ctl00_phContent_gvPlanningRegister").search('tr')[1..-1].each do |r|
  record = {
    'info_url' => (page.uri + r.at('a')['href']).to_s,
    'comment_url' => "mailto:council@stonnington.vic.gov.au",
    'council_reference' => r.search('td')[0].inner_text,
    'date_received' => Date.strptime(r.search('td')[1].inner_text.strip, '%d/%m/%Y').to_s,
    'address' => r.search('td')[3].inner_text.strip + ", VIC",
    'description' => r.search('td')[4].inner_text.strip,
    'date_scraped' => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end