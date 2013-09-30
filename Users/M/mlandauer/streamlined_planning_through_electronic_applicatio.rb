# Migrated this scraper from https://github.com/openaustralia/planningalerts-parsers/blob/master/lib/spear_scraper.rb

require 'mechanize'

# Extracts all the data on a single page of results
def extract_page_data(page)
  comment_url = "https://www.spear.land.vic.gov.au/spear/pages/public-and-other-users/objectors.shtml"

  apps = []
  # Skip first two row (header) and last row (page navigation)
  page.at('div#list table').search('tr')[2..-2].each do |row|
    values = row.search('td')
    
    # Type appears to be either something like "Certification of a Plan" or "Planning Permit and Certification"
    # I think we need to look in detail at the application to get the description
    # TODO: Figure out whether we should ignore "Certification of a Plan"
    #type = values[3].inner_html.strip
    #status = values[4].inner_html.strip
    # I'm going to take a punt here on what the correct thing to do is - I think if there is a link available to
    # the individual planning application that means that it's something that requires deliberation and so interesting.
    # I'm going to assume that everything else is purely "procedural" and should not be recorded here

    # If there is a link on the address record this development application
    if values[0].at('a')
      info_url = (page.uri + URI.parse(values[0].at('a').attributes['href'])).to_s
      record = {
        # We're using the SPEAR Ref # because we want that to be unique across the "authority"
        'council_reference' => values[8].inner_html.strip,
        'address' => values[0].at('a').inner_html.strip,
        'date_received' => Date.strptime(values[10].inner_html.strip, "%d/%m/%Y").to_s,
        'info_url' => info_url,
        'comment_url' => comment_url,
        'date_scraped' => Date.today.to_s
      }

      if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
        # Get more detailed information by going to the application detail page (but only if necessary)
        record["description"] = extract_description(info_url)
        #p record
        ScraperWiki.save_sqlite(['council_reference'], record)
      else
        #puts "Skipping already saved record " + record['council_reference']
      end

    end
  end
end

# Get a description of the application extracted from the more detailed information page (at info_url)
def extract_description(info_url)
  agent = Mechanize.new
  agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

  page = agent.get(info_url)

  # The horrible thing about this page is they use tables for layout. Well done!
  # Also I think the "Intended use" bit looks like the most useful. So, we'll use that for the description
  table = page.at('div#bodypadding table')
  # For some reason occasionaly this page can be entirely blank. If it is just do our best and continue
  if table
    table.search('table')[1].search('tr').find do |row|
      # <th> tag contains the name of the field, <td> tag contains its value
      row.at('th') && row.at('th').inner_text.strip == "Intended use"
    end.at('td').inner_text.strip
  end
end

def applications(web_form_name)
  url = "http://www.spear.land.vic.gov.au/spear/publicSearch/Search.do"

  agent = Mechanize.new
  # Doing this as a workaround because there don't appear to be root certificates for Ruby 1.9 installed on
  # Scraperwiki. Doesn't really make any difference because we're not sending anything requiring any kind
  # of security back and forth
  agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

  page = agent.get(url)
  form = page.forms.first
  # TODO: Is there a more sensible way to pick the item in the drop-down?
  form.field_with(:name => "councilName").options.find{|o| o.text == web_form_name}.click
  page = form.submit
  
  begin
    extract_page_data(page)
    next_link = page.link_with(:text => /next/)
    page = next_link.click if next_link
  end until next_link.nil? 
end

url = "http://www.spear.land.vic.gov.au/spear/publicSearch/Search.do"

agent = Mechanize.new
agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

page = agent.get(url)
form = page.forms.first
council_names = form.field_with(:name => "councilName").options.map{|o| o.text}[1..-1]

council_names.each do |council_name|
  puts "Scraping #{council_name}..."
  applications(council_name)
end

# Migrated this scraper from https://github.com/openaustralia/planningalerts-parsers/blob/master/lib/spear_scraper.rb

require 'mechanize'

# Extracts all the data on a single page of results
def extract_page_data(page)
  comment_url = "https://www.spear.land.vic.gov.au/spear/pages/public-and-other-users/objectors.shtml"

  apps = []
  # Skip first two row (header) and last row (page navigation)
  page.at('div#list table').search('tr')[2..-2].each do |row|
    values = row.search('td')
    
    # Type appears to be either something like "Certification of a Plan" or "Planning Permit and Certification"
    # I think we need to look in detail at the application to get the description
    # TODO: Figure out whether we should ignore "Certification of a Plan"
    #type = values[3].inner_html.strip
    #status = values[4].inner_html.strip
    # I'm going to take a punt here on what the correct thing to do is - I think if there is a link available to
    # the individual planning application that means that it's something that requires deliberation and so interesting.
    # I'm going to assume that everything else is purely "procedural" and should not be recorded here

    # If there is a link on the address record this development application
    if values[0].at('a')
      info_url = (page.uri + URI.parse(values[0].at('a').attributes['href'])).to_s
      record = {
        # We're using the SPEAR Ref # because we want that to be unique across the "authority"
        'council_reference' => values[8].inner_html.strip,
        'address' => values[0].at('a').inner_html.strip,
        'date_received' => Date.strptime(values[10].inner_html.strip, "%d/%m/%Y").to_s,
        'info_url' => info_url,
        'comment_url' => comment_url,
        'date_scraped' => Date.today.to_s
      }

      if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
        # Get more detailed information by going to the application detail page (but only if necessary)
        record["description"] = extract_description(info_url)
        #p record
        ScraperWiki.save_sqlite(['council_reference'], record)
      else
        #puts "Skipping already saved record " + record['council_reference']
      end

    end
  end
end

# Get a description of the application extracted from the more detailed information page (at info_url)
def extract_description(info_url)
  agent = Mechanize.new
  agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

  page = agent.get(info_url)

  # The horrible thing about this page is they use tables for layout. Well done!
  # Also I think the "Intended use" bit looks like the most useful. So, we'll use that for the description
  table = page.at('div#bodypadding table')
  # For some reason occasionaly this page can be entirely blank. If it is just do our best and continue
  if table
    table.search('table')[1].search('tr').find do |row|
      # <th> tag contains the name of the field, <td> tag contains its value
      row.at('th') && row.at('th').inner_text.strip == "Intended use"
    end.at('td').inner_text.strip
  end
end

def applications(web_form_name)
  url = "http://www.spear.land.vic.gov.au/spear/publicSearch/Search.do"

  agent = Mechanize.new
  # Doing this as a workaround because there don't appear to be root certificates for Ruby 1.9 installed on
  # Scraperwiki. Doesn't really make any difference because we're not sending anything requiring any kind
  # of security back and forth
  agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

  page = agent.get(url)
  form = page.forms.first
  # TODO: Is there a more sensible way to pick the item in the drop-down?
  form.field_with(:name => "councilName").options.find{|o| o.text == web_form_name}.click
  page = form.submit
  
  begin
    extract_page_data(page)
    next_link = page.link_with(:text => /next/)
    page = next_link.click if next_link
  end until next_link.nil? 
end

url = "http://www.spear.land.vic.gov.au/spear/publicSearch/Search.do"

agent = Mechanize.new
agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

page = agent.get(url)
form = page.forms.first
council_names = form.field_with(:name => "councilName").options.map{|o| o.text}[1..-1]

council_names.each do |council_name|
  puts "Scraping #{council_name}..."
  applications(council_name)
end

