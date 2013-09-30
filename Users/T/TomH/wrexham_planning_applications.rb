require "rubygems"
require "mechanize"
require "date"

# Output a log message
def log(message)
  puts "#{Time.now.strftime('%Y-%m-%d %H:%M:%S')} #{message}"
end

# Create and configure a user agent
def get_user_agent
  # Create a user agent
  agent = Mechanize.new
  
  # Set the user agent - the standard mechanize agent does not work!
  agent.user_agent_alias = "Linux Mozilla"

  # Disable automatic redirect processing
  agent.redirect_ok = false

  # Allow POST requests to be retried
  agent.retry_change_requests = true

  # This is important as everything seems to fail without it...
  agent.get("http://planning.wrexham.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningWelcome.page")

  agent
end

# Cleanup an address
def clean_address(address)
  if match = address.match(/ *((?:CM|IP)[0-9]{1,2}) *([0-9][a-z]{2}) *$/i)
    postcode = "#{match[1].upcase} #{match[2].upcase}"
    address[match.begin(0),match.end(0)] = " #{postcode}"
  end

  return address, postcode
end

# Process search results
def process_search_results(agent, to_date, from_date, page)
  # Don't know page details yet
  current_page = 0
  total_pages = 0

  # Find the number of pages and the current page
  page.root.css("table.scroller").each do |scroller|
    current_page = scroller.css("td[@style!='']").first.content.to_i
    total_pages = scroller.css("td").last.previous.previous.content.to_i
  end

  # There seems to be a limit of 5 pages, so if we hit it then split things up
  if total_pages == 5
    # Find the mid point...
    mid_date = from_date + ( to_date - from_date ) / 2

    # ...and search either side of it
    search_for_applications(mid_date, from_date, agent)
    search_for_applications(to_date, mid_date + 1, agent)
  else
    # Find the results table
    page.root.css("tbody").each do |table|
      # Loop over the result rows
      table.css("tr").each do |row|
        columns = row.css("td")
        record = {}

        record[:uid] = columns[0].css("input").first["value"]
        record[:date_received] = Date.strptime(columns[1].content, "%d/%m/%Y")
        record[:address] = columns[2].content
        record[:description] = columns[3].content

        record[:start_date] = record[:date_received]

        if ScraperWiki.select("* FROM swdata WHERE uid = '#{record[:uid]}'").empty? 
          ScraperWiki.save([:uid], record)
        end
      end
    end

    # If we're not the last page then get the next one and process it
    if current_page < total_pages
      scroller = page.form_with(:id => "_id426")
      scroller["_id426:scroll_1"] = "next"
      search_results = agent.submit(scroller)
      process_search_results(agent, to_date, from_date, search_results)
    end
  end
end

# Search for planning applications in a given date range
def search_for_applications(to_date = Date.today, from_date = to_date - 14, agent = get_user_agent)
  # Tell the user what we're doing
  log "Searching for applications between #{from_date} and #{to_date}"

  # Get the search page and submit the search
  search_page = agent.get("http://planning.wrexham.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning")
  search_form = search_page.form_with(:id => "_id423")
  search_form["_id423:SDate1From"] = from_date.strftime("%d/%m/%Y")
  search_form["_id423:SDate1To"] = to_date.strftime("%d/%m/%Y")
  search_button = search_form.button_with(:id => "_id423:_id439")
  search_results = agent.submit(search_form, search_button)
  
  # Process the results - will recursively fetch additional pages
  process_search_results(agent, to_date, from_date, search_results)
end

# Update details for an application
def update_application(agent, record)
  # Get the search page and submit the search
  search_page = agent.get("http://planning.wrexham.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning")
  search_form = search_page.form_with(:id => "_id423")
  search_form["_id423:SDescription"] = record["uid"]
  search_button = search_form.button_with(:id => "_id423:_id439")
  search_result = agent.submit(search_form, search_button)

  # Find the table with the address details and extract them
  search_result.root.css("table[@title='Address Details'] tbody").each do |table|
    address = []

    table.css("tr").each do |row|
      name = row.css("td.planSResultcol1").first.content
      value = row.css("td.planSResultcol2").first.content

      if value.length > 0
        case name
        when "Address", "Address 2", "Address 3", "Address 4", "Address 5"; address.push(value)
        when "Postcode"; record[:postcode] = value
        # Community
        when "Ward"; record[:ward_name] = value
        end
      end
    end

    record[:address] = address.join(", ")

    if record[:postcode]
      record[:address] = record[:address] + " " + record[:postcode]
    end
  end

  # Find the table with the case details and extract them
  search_result.root.css("table[@title='Case Details'] tbody").each do |table|
    table.css("tr").each do |row|
      name = row.css("td.planSResultcol1").first.content
      value = row.css("td.planSResultcol2").first.content

      if value.length > 0
        case name
        when "Received Date"; record[:date_received] = Date.strptime(value, "%d/%m/%Y")
        when "Case Officer Initials"; record[:case_officer] = value
        when "Proposed development"; record[:description] = value
        when "Decision"; record[:decision] = value
        end
      end
    end
  end

  # Look for mention of a related application
  if record[:description] and
     match = record[:description].match(/([0-9]+\/[0-9]+\/[0-9]+\/[A-Z]+(?:\/[A-Z]+)?)/i)
    record[:associated_application_uid] = match[1].upcase
  end

  # Fill in other fields
  record[:start_date] = [record[:date_received], record[:date_validated]].compact.min
  record[:date_scraped] = Time.now

  # Save the updated record
  ScraperWiki.save([:uid], record)
end

# Update details for stale applications
def update_stale_applications(since_date = Date.today - 60)
  # Get a user agent
  agent = get_user_agent

  # Tell the user what we're doing
  log "Updating recent applications"

  # Update the details for any recent applications
  ScraperWiki.select("* FROM swdata WHERE start_date IS NULL OR start_date > '#{since_date.strftime('%F')}' ORDER BY date_scraped LIMIT 500").each do |record|
    update_application(agent, record)
  end

  # Tell the user what we're doing
  log "Loading pending applications"

  # Get the details for any applications we haven't scraped yet
  ScraperWiki.select("* FROM swdata WHERE date_scraped IS NULL LIMIT 500").each do |record|
    update_application(agent, record)
  end
end

search_for_applications
update_stale_applications

require "rubygems"
require "mechanize"
require "date"

# Output a log message
def log(message)
  puts "#{Time.now.strftime('%Y-%m-%d %H:%M:%S')} #{message}"
end

# Create and configure a user agent
def get_user_agent
  # Create a user agent
  agent = Mechanize.new
  
  # Set the user agent - the standard mechanize agent does not work!
  agent.user_agent_alias = "Linux Mozilla"

  # Disable automatic redirect processing
  agent.redirect_ok = false

  # Allow POST requests to be retried
  agent.retry_change_requests = true

  # This is important as everything seems to fail without it...
  agent.get("http://planning.wrexham.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningWelcome.page")

  agent
end

# Cleanup an address
def clean_address(address)
  if match = address.match(/ *((?:CM|IP)[0-9]{1,2}) *([0-9][a-z]{2}) *$/i)
    postcode = "#{match[1].upcase} #{match[2].upcase}"
    address[match.begin(0),match.end(0)] = " #{postcode}"
  end

  return address, postcode
end

# Process search results
def process_search_results(agent, to_date, from_date, page)
  # Don't know page details yet
  current_page = 0
  total_pages = 0

  # Find the number of pages and the current page
  page.root.css("table.scroller").each do |scroller|
    current_page = scroller.css("td[@style!='']").first.content.to_i
    total_pages = scroller.css("td").last.previous.previous.content.to_i
  end

  # There seems to be a limit of 5 pages, so if we hit it then split things up
  if total_pages == 5
    # Find the mid point...
    mid_date = from_date + ( to_date - from_date ) / 2

    # ...and search either side of it
    search_for_applications(mid_date, from_date, agent)
    search_for_applications(to_date, mid_date + 1, agent)
  else
    # Find the results table
    page.root.css("tbody").each do |table|
      # Loop over the result rows
      table.css("tr").each do |row|
        columns = row.css("td")
        record = {}

        record[:uid] = columns[0].css("input").first["value"]
        record[:date_received] = Date.strptime(columns[1].content, "%d/%m/%Y")
        record[:address] = columns[2].content
        record[:description] = columns[3].content

        record[:start_date] = record[:date_received]

        if ScraperWiki.select("* FROM swdata WHERE uid = '#{record[:uid]}'").empty? 
          ScraperWiki.save([:uid], record)
        end
      end
    end

    # If we're not the last page then get the next one and process it
    if current_page < total_pages
      scroller = page.form_with(:id => "_id426")
      scroller["_id426:scroll_1"] = "next"
      search_results = agent.submit(scroller)
      process_search_results(agent, to_date, from_date, search_results)
    end
  end
end

# Search for planning applications in a given date range
def search_for_applications(to_date = Date.today, from_date = to_date - 14, agent = get_user_agent)
  # Tell the user what we're doing
  log "Searching for applications between #{from_date} and #{to_date}"

  # Get the search page and submit the search
  search_page = agent.get("http://planning.wrexham.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning")
  search_form = search_page.form_with(:id => "_id423")
  search_form["_id423:SDate1From"] = from_date.strftime("%d/%m/%Y")
  search_form["_id423:SDate1To"] = to_date.strftime("%d/%m/%Y")
  search_button = search_form.button_with(:id => "_id423:_id439")
  search_results = agent.submit(search_form, search_button)
  
  # Process the results - will recursively fetch additional pages
  process_search_results(agent, to_date, from_date, search_results)
end

# Update details for an application
def update_application(agent, record)
  # Get the search page and submit the search
  search_page = agent.get("http://planning.wrexham.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning")
  search_form = search_page.form_with(:id => "_id423")
  search_form["_id423:SDescription"] = record["uid"]
  search_button = search_form.button_with(:id => "_id423:_id439")
  search_result = agent.submit(search_form, search_button)

  # Find the table with the address details and extract them
  search_result.root.css("table[@title='Address Details'] tbody").each do |table|
    address = []

    table.css("tr").each do |row|
      name = row.css("td.planSResultcol1").first.content
      value = row.css("td.planSResultcol2").first.content

      if value.length > 0
        case name
        when "Address", "Address 2", "Address 3", "Address 4", "Address 5"; address.push(value)
        when "Postcode"; record[:postcode] = value
        # Community
        when "Ward"; record[:ward_name] = value
        end
      end
    end

    record[:address] = address.join(", ")

    if record[:postcode]
      record[:address] = record[:address] + " " + record[:postcode]
    end
  end

  # Find the table with the case details and extract them
  search_result.root.css("table[@title='Case Details'] tbody").each do |table|
    table.css("tr").each do |row|
      name = row.css("td.planSResultcol1").first.content
      value = row.css("td.planSResultcol2").first.content

      if value.length > 0
        case name
        when "Received Date"; record[:date_received] = Date.strptime(value, "%d/%m/%Y")
        when "Case Officer Initials"; record[:case_officer] = value
        when "Proposed development"; record[:description] = value
        when "Decision"; record[:decision] = value
        end
      end
    end
  end

  # Look for mention of a related application
  if record[:description] and
     match = record[:description].match(/([0-9]+\/[0-9]+\/[0-9]+\/[A-Z]+(?:\/[A-Z]+)?)/i)
    record[:associated_application_uid] = match[1].upcase
  end

  # Fill in other fields
  record[:start_date] = [record[:date_received], record[:date_validated]].compact.min
  record[:date_scraped] = Time.now

  # Save the updated record
  ScraperWiki.save([:uid], record)
end

# Update details for stale applications
def update_stale_applications(since_date = Date.today - 60)
  # Get a user agent
  agent = get_user_agent

  # Tell the user what we're doing
  log "Updating recent applications"

  # Update the details for any recent applications
  ScraperWiki.select("* FROM swdata WHERE start_date IS NULL OR start_date > '#{since_date.strftime('%F')}' ORDER BY date_scraped LIMIT 500").each do |record|
    update_application(agent, record)
  end

  # Tell the user what we're doing
  log "Loading pending applications"

  # Get the details for any applications we haven't scraped yet
  ScraperWiki.select("* FROM swdata WHERE date_scraped IS NULL LIMIT 500").each do |record|
    update_application(agent, record)
  end
end

search_for_applications
update_stale_applications

