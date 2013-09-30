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

  agent
end

# Cleanup an address
def clean_address(address)
  if match = address.match(/ *((?:HA|UB)[0-9]{1,2}) *([0-9][a-z]{2}) *$/i)
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
  page.root.css("div.scroller").each do |scroller|
    if match = scroller.content.match(/Page ([0-9]+) of ([0-9]+)/)
      current_page = match[1].to_i
      total_pages = match[2].to_i
    end
  end

  # There seems to be a limit of 10 pages, so if we hit it then split things up
  if total_pages == 10
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

        record[:uid] = columns[0].content
        record[:applicant_name] = columns[1].content
        record[:agent_name] = columns[2].content
     #   record[:application_type] = columns[3].content
        record[:status] = columns[4].content
        record[:address] = columns[5].content
        record[:ward_name] = columns[6].content
        record[:date_validated] = Date.strptime(columns[7].content, "%d/%m/%Y")
        record[:postcode] = columns[8].content
        record[:start_date] = record[:date_validated]

        if ScraperWiki.select("* FROM swdata WHERE uid = '#{record[:uid]}'").empty? 
          ScraperWiki.save([:uid], record)
        end
      end
    end

    # If we're not the last page then get the next one and process it
    if current_page < total_pages
      scroller = page.form_with(:id => "_id61")
      scroller["_id61:scroll_2"] = "next"
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
  search_page = agent.get("http://www.harrow.gov.uk/planningsearch/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=planningsearch&Param=lg.Planning&searchType=quick")
  search_form = search_page.form_with(:id => "_id185")
  search_form["_id185:SDate2From"] = from_date.strftime("%d/%m/%Y")
  search_form["_id185:SDate2To"] = to_date.strftime("%d/%m/%Y")
  search_button = search_form.button_with(:id => "_id185:_id273")
  search_results = agent.submit(search_form, search_button)
  
  # Process the results - will recursively fetch additional pages
  process_search_results(agent, to_date, from_date, search_results)
end

# Update details for an application
def update_application(agent, record)
  # Get the search page and submit the search
  search_page = agent.get("http://www.harrow.gov.uk/planningsearch/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=planningsearch&Param=lg.Planning&searchType=quick")
  search_form = search_page.form_with(:id => "_id164")
  search_form["_id164:SDescription"] = record["uid"]
  search_button = search_form.button_with(:id => "_id164:_id266")
  search_result = agent.submit(search_form, search_button)

  # Select the right result if we got more than one match
  if search_form = search_result.form_with(:id => "_id61")
    if search_form.button_with(:value => "View Details")
      search_result.root.css("form#_id61 tbody tr").each do |row|
        if row.css("td").first.content == record["uid"]
          search_button = search_form.button_with(:id => row.css("input").first.attr("id"))
        end
      end

      search_result = agent.submit(search_form, search_button)
    end
  end

  # Find the table with the address details and extract them
  search_result.root.css("table tbody").each do |table|
    table.css("tr").each do |row|
      if row.css("td.label").first and row.css("td.data").first
        name = row.css("td.label").first.content
        value = row.css("td.data").first.content

        if value.length > 0
          case name
       #   when "Location"; record[:address], record[:postcode] = clean_address(value)
          when "Postcode"; record[:postcode] = value
          when "Ward"; record[:ward_name] = value
          when "Agent Name"; record[:agent_name] = value
          when "Agent Address"; record[:agent_address] = clean_address(value).first
          when "Applicant Name"; record[:applicant_name] = value
       #   when "Application"; record[:application_type] = value
          when "Date Registered"; record[:date_validated] = Date.strptime(value, "%d/%m/%Y")
          when "Application Type"; record[:application_type] = value
          when "Case Officer"; record[:case_officer] = value
          when "Proposal"; record[:description] = value
          when "Decision"; record[:decision] = value
          when "Decision Date"; record[:decision_date] = Date.strptime(value, "%d/%m/%Y")
          when "Status"; record[:status] = value
          when "Appeal Lodged Date"; record[:appeal_date] = Date.strptime(value, "%d/%m/%Y")
          end
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
  record[:start_date] = record[:date_validated]
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

  agent
end

# Cleanup an address
def clean_address(address)
  if match = address.match(/ *((?:HA|UB)[0-9]{1,2}) *([0-9][a-z]{2}) *$/i)
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
  page.root.css("div.scroller").each do |scroller|
    if match = scroller.content.match(/Page ([0-9]+) of ([0-9]+)/)
      current_page = match[1].to_i
      total_pages = match[2].to_i
    end
  end

  # There seems to be a limit of 10 pages, so if we hit it then split things up
  if total_pages == 10
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

        record[:uid] = columns[0].content
        record[:applicant_name] = columns[1].content
        record[:agent_name] = columns[2].content
     #   record[:application_type] = columns[3].content
        record[:status] = columns[4].content
        record[:address] = columns[5].content
        record[:ward_name] = columns[6].content
        record[:date_validated] = Date.strptime(columns[7].content, "%d/%m/%Y")
        record[:postcode] = columns[8].content
        record[:start_date] = record[:date_validated]

        if ScraperWiki.select("* FROM swdata WHERE uid = '#{record[:uid]}'").empty? 
          ScraperWiki.save([:uid], record)
        end
      end
    end

    # If we're not the last page then get the next one and process it
    if current_page < total_pages
      scroller = page.form_with(:id => "_id61")
      scroller["_id61:scroll_2"] = "next"
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
  search_page = agent.get("http://www.harrow.gov.uk/planningsearch/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=planningsearch&Param=lg.Planning&searchType=quick")
  search_form = search_page.form_with(:id => "_id185")
  search_form["_id185:SDate2From"] = from_date.strftime("%d/%m/%Y")
  search_form["_id185:SDate2To"] = to_date.strftime("%d/%m/%Y")
  search_button = search_form.button_with(:id => "_id185:_id273")
  search_results = agent.submit(search_form, search_button)
  
  # Process the results - will recursively fetch additional pages
  process_search_results(agent, to_date, from_date, search_results)
end

# Update details for an application
def update_application(agent, record)
  # Get the search page and submit the search
  search_page = agent.get("http://www.harrow.gov.uk/planningsearch/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=planningsearch&Param=lg.Planning&searchType=quick")
  search_form = search_page.form_with(:id => "_id164")
  search_form["_id164:SDescription"] = record["uid"]
  search_button = search_form.button_with(:id => "_id164:_id266")
  search_result = agent.submit(search_form, search_button)

  # Select the right result if we got more than one match
  if search_form = search_result.form_with(:id => "_id61")
    if search_form.button_with(:value => "View Details")
      search_result.root.css("form#_id61 tbody tr").each do |row|
        if row.css("td").first.content == record["uid"]
          search_button = search_form.button_with(:id => row.css("input").first.attr("id"))
        end
      end

      search_result = agent.submit(search_form, search_button)
    end
  end

  # Find the table with the address details and extract them
  search_result.root.css("table tbody").each do |table|
    table.css("tr").each do |row|
      if row.css("td.label").first and row.css("td.data").first
        name = row.css("td.label").first.content
        value = row.css("td.data").first.content

        if value.length > 0
          case name
       #   when "Location"; record[:address], record[:postcode] = clean_address(value)
          when "Postcode"; record[:postcode] = value
          when "Ward"; record[:ward_name] = value
          when "Agent Name"; record[:agent_name] = value
          when "Agent Address"; record[:agent_address] = clean_address(value).first
          when "Applicant Name"; record[:applicant_name] = value
       #   when "Application"; record[:application_type] = value
          when "Date Registered"; record[:date_validated] = Date.strptime(value, "%d/%m/%Y")
          when "Application Type"; record[:application_type] = value
          when "Case Officer"; record[:case_officer] = value
          when "Proposal"; record[:description] = value
          when "Decision"; record[:decision] = value
          when "Decision Date"; record[:decision_date] = Date.strptime(value, "%d/%m/%Y")
          when "Status"; record[:status] = value
          when "Appeal Lodged Date"; record[:appeal_date] = Date.strptime(value, "%d/%m/%Y")
          end
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
  record[:start_date] = record[:date_validated]
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
