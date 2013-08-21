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

  # Allow POST requests to be retried
  agent.retry_change_requests = true

  # Add an "allows cookies" cookie
  agent.cookie_jar << Mechanize::Cookie.new("cwallowcookies", "true", :domain => "www.southsomerset.gov.uk", :path => "/planning-and-building-control/planning-search/")

  # Add an "Agreed to Statement of Purpose" cookie
  agent.cookie_jar << Mechanize::Cookie.new("plnSOP", "yes", :domain => "www.southsomerset.gov.uk", :path => "/")

  agent
end

# Cleanup an address
def clean_address(address)
  lines = address.split(/\s*,\s*/)

  if match = lines[-1].match(/((?:BA|DT|TA)[0-9]{1,2}) *([0-9][a-z]{2})$/i)
    postcode = lines[-1] = "#{match[1].upcase} #{match[2].upcase}"
  end

  address = lines[0..-1].join(", ")

  return address, postcode
end

# Process search results
def process_search_results(agent, page)
  # Loop over the result rows adding records
  page.root.css("table#ContentPlaceHolderDefault_cphBody_cphBody_ctl02_SSDCPlanningResults_5_grdPlanningResults > tr").each do |row|
    columns = row.xpath("./td")

    if columns.count == 5
      record = {}

      record[:uid] = columns[0].content
      record[:date_received] = Date.strptime(columns[1].content, "%d-%b-%Y")
      record[:address], record[:postcode] = clean_address(columns[2].content)
      record[:description] = columns[3].content
      record[:decision] = columns[4].content
      record[:start_date] = record[:date_received]

      if ScraperWiki.select("* FROM swdata WHERE uid = '#{record[:uid]}'").empty? 
        ScraperWiki.save([:uid], record)
      end
    elsif columns.count == 1
      current_page = columns[0].css("td > span").first.content.to_i
      last_page = columns[0].css("td").last.content

      if last_page == "..." or current_page < last_page.to_i
        new_page = current_page + 1
 
        formPrefix = "ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault"

        form = page.form_with(:id => "frmMain")
        form["__EVENTTARGET"] = "#{formPrefix}$cphBody$cphBody$ctl02$SSDCPlanningResults_5$grdPlanningResults"
        form["__EVENTARGUMENT"] = "Page$#{new_page}"
        search_results = agent.submit(form)

        process_search_results(agent, search_results)
      end
    end
  end
end

# Search for planning applications in a given date range
def search_for_applications(to_date = Date.today, from_date = to_date - 14, agent = get_user_agent)
  # Are we looking for more than 21 days worth?
  if to_date - from_date > 21
    # Yes, so find the mid point...
    mid_date = from_date + ( to_date - from_date ) / 2

    # ...and search either side of it
    search_for_applications(mid_date, from_date, agent)
    search_for_applications(to_date, mid_date + 1, agent)
  else
    # Tell the user what we're doing
    log "Searching for applications between #{from_date} and #{to_date}"

    # Format the start and end dates
    from_date = from_date.strftime("%d-%b-%Y")
    to_date = to_date.strftime("%d-%b-%Y")

    # Do the search
    search_results = agent.get("http://www.southsomerset.gov.uk/planning-and-building-control/planning-search/search-results.aspx?startdate=#{from_date}&enddate=#{to_date}")

    # Process the results
    process_search_results(agent, search_results)

    # Discard the page
    search_results.reset
  end
end

# Parse a date
def parse_date(date)
  Date.strptime(date, "%d-%b-%Y") unless date == "No details"
end

# Update details for an application
def update_application(agent, record)
  # Get the ID for the query
  id = record["uid"].gsub("/", "")

  # Fill in the URL
  record[:url] = "http://www.southsomerset.gov.uk/planning-and-building-control/planning-search/full-details.aspx?id=#{id}"

  # Get the application details
  details_page = agent.get(record[:url])

  # Extract application details
  details_page.root.css("div.tab_container").css("div#fragment1,div#fragment2,div#fragment3").css("td").each do |value|
    if value.previous and not value.css("div").first
      name = value.previous.inner_html.gsub(/\s*<br>\s*/, " ")

      if name.length > 0 and value.content.length > 0
        case name
          when "Application No:";
          when "Type of application:"; record[:application_type] = value.content
          when "Proposal:"; record[:description] = value.content
          when "Address:";
          when "Ward: Parish: Area:"; record[:ward], record[:parish] = value.inner_html.split(/\s*<br>\s*/)
          when "Case officer:"; record[:case_officer] = value.content
          when "Status:"; record[:status] = value.content
          when "Decision:"; record[:decision] = value.content
          when "Appeal status:"; record[:appeal_decision] = value.content
          when "Application received:"; record[:date_received] = parse_date(value.content)
          when "Application validated:"; record[:date_validated] = parse_date(value.content)
          when "Target date:"; record[:target_decision_date] = parse_date(value.content)
          when "Target committee:"; record[:meeting_date] = parse_date(value.content)
          when "Actual committee:"; record[:meeting_date] = parse_date(value.content)
          when "Neighbour consultations sent on:"; record[:neighbour_consultation_start_date] = parse_date(value.content)
          when "Expiry date for neighbour consultations:"; record[:neighbour_consultation_end_date] = parse_date(value.content)
          when "Standard consultations sent on:"; record[:consultation_start_date] = parse_date(value.content)
          when "Expiry date for standard consultations:"; record[:consultation_end_date] = parse_date(value.content)
          when "Overall expiry date:";
          when "Decision made:"; record[:decision_date] = parse_date(value.content)
          when "Appeal decision date:"; record[:appeal_decision_date] = parse_date(value.content)
          when "Applicants name:"; record[:applicant_name] = value.content
          when "Agents name:"; record[:agent_name] = value.content
          when "Agents address:"; record[:agent_address] = value.content.gsub("\n", ", ")
          else; log "#{name} @ #{value.content}"
        end
      end
    end
  end

  # Fill in other fields
  record[:start_date] = [record[:date_received], record[:date_validated]].compact.min
  record[:date_scraped] = Time.now

  # Save the updated record
  ScraperWiki.save([:uid], record)
rescue Exception => ex
  # Log error
  log "Failed to fetch details for #{record["uid"]}: #{ex.to_s}"
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
