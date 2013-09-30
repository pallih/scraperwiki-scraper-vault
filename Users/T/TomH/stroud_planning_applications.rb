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

  agent
end

# Parse the "Decision Notice" field
def parse_decision_notice(decision_notice, record)
  if decision_notice =~ /^\s*A decision has not yet been made\s*$/
    # Nothing to record
  elsif decision_notice =~ /^\s*We dispatched the decision notice on (\d{1,2} \w{3} \d{4})\s*$/
    record[:decision_issued_date] = Date.strptime($1, "%d %b %Y")
  else
    throw "Can't parse decision notice: #{decision_notice}"
  end
end

# Parse the "Appeal Status" field
def parse_appeal_status(appeal_status, link, record, agent)
  if appeal_status =~ /^\s*No Appeal Found\s*$/
    # Nothing to record
  elsif appeal_status =~ /^\s*This decision was appealed on (\d{1,2} \w{3} \d{4}) and the appeal is in progress./
    record[:appeal_date] = Date.strptime($1, "%d %b %Y")
  elsif appeal_status =~ /^\s*This decision was appealed on (\d{1,2} \w{3} \d{4}) and decided on (\d{1,2} \w{3} \d{4})./
    record[:appeal_date] = Date.strptime($1, "%d %b %Y")
    record[:appeal_decision_date] = Date.strptime($2, "%d %b %Y")
  elsif appeal_status =~ /^\s*This decision was appealed on\s+and decided on (\d{1,2} \w{3} \d{4})./
    record[:appeal_decision_date] = Date.strptime($1, "%d %b %Y")
  else
    throw "Can't parse appeal status for #{record[:uid]}: #{appeal_status}"
  end

  if link
    appeals = agent.get(link)

    appeals.root.css("table.tablesorter > tbody > tr").each_slice(2) do |summary,details|
      columns = summary.css("td")

      if columns[1].content.strip == record[:uid]
        record[:appeal_result] = columns[5].content.strip
      end
    end
  end
end

# Process search results
def process_search_results(agent, page)
  page.root.css("table.tablesorter > tbody > tr").each_slice(2) do |summary,details|
    columns = summary.css("td")
    record = {}

    # Extract summary information
    record[:uid] = columns[1].content.strip
    record[:address] = columns[2].content.strip
    record[:description] = columns[3].content.strip
    record[:status] = columns[4].content.strip

    # Parse the details table
    details.css("table").first.css("tr").each do |row|
      columns = row.css("td")
      name = columns[0].content.strip
      value = columns[1].content.strip

      if link = columns[1].css("a").first
        link = link.attr("href")
      end

      if value.length > 0 and value != "N/A"
        case name
          when "Applicant Name"; record[:applicant_name] = value
          when "Agent Name"; record[:agent_name] = value
#          when "Delegation"; record[] = value
          when "Handling Officer"; record[:case_officer] = value
          when "Application Type"; record[:application_type] = value
#          when "Listed Building"; record[] = value
          when "Parish"; record[:parish] = value
          when "Ward"; record[:ward_name] = value
#          when "Newspaper Name"; record[] = value
          when "Publication Date"; record[:last_advertised_date] = Date.strptime(value, "%d %b %Y")
          when "Application received on"; record[:date_received] = Date.strptime(value, "%d %b %Y")
          when "Application validated on"; record[:date_validated] = Date.strptime(value, "%d %b %Y")
          when "Decision Notice"; parse_decision_notice(value, record)
          when "Appeal Status"; parse_appeal_status(value, link, record, agent)
#          when "Calculated Fee"; record[] = value
#          when "Fee Paid"; record[] = value
        end
      end
    end

    # Fill in other fields
    record[:comment_url] = "http://www.stroud.gov.uk/PLO/PlanningComments.aspx?par=#{record[:uid]}"
    record[:start_date] = [record[:date_received], record[:date_validated]].compact.min
    record[:date_scraped] = Time.now

    # Save the record
    ScraperWiki.save([:uid], record)
  end
end

# Search for planning applications in a given date range
def search_for_applications(to_date = Date.today, from_date = to_date - 60, agent = get_user_agent)
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

    # Get the search page
    search_page = agent.get("http://www.stroud.gov.uk/PLO/Default.aspx")

    # Submit the search
    search_form = search_page.form_with(:id => "form1")
    search_form.field_with(:id => "receivedafter").value = from_date.strftime("%d/%m/%Y")
    search_form.field_with(:id => "receivedb4").value = to_date.strftime("%d/%m/%Y")
    search_form.radiobutton_with(:id => "ApplicationDecided_1").check
    search_button = search_form.button_with(:id => "Button41")
    search_results = agent.submit(search_form, search_button)

    # Process the results
    process_search_results(agent, search_results)

    # Discard the page
    search_results.reset
  end
end

# Search for recent decisions
def search_for_decisions
  # Get a user agent
  agent = get_user_agent

  # Tell the user what we're doing
  log "Searching for recent decisions"

  # Get the search page
  search_page = agent.get("http://www.stroud.gov.uk/PLO/Default.aspx")

  # Submit the search
  search_form = search_page.form_with(:id => "form1")
  search_form["__EVENTTARGET"] = "ctl00$MainContent$LinkButton4"
  search_form["__EVENTARGUMENT"] = ""
  search_results = agent.submit(search_form)

  # Process the results
  process_search_results(agent, search_results)
end

search_for_applications
search_for_decisions
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

  agent
end

# Parse the "Decision Notice" field
def parse_decision_notice(decision_notice, record)
  if decision_notice =~ /^\s*A decision has not yet been made\s*$/
    # Nothing to record
  elsif decision_notice =~ /^\s*We dispatched the decision notice on (\d{1,2} \w{3} \d{4})\s*$/
    record[:decision_issued_date] = Date.strptime($1, "%d %b %Y")
  else
    throw "Can't parse decision notice: #{decision_notice}"
  end
end

# Parse the "Appeal Status" field
def parse_appeal_status(appeal_status, link, record, agent)
  if appeal_status =~ /^\s*No Appeal Found\s*$/
    # Nothing to record
  elsif appeal_status =~ /^\s*This decision was appealed on (\d{1,2} \w{3} \d{4}) and the appeal is in progress./
    record[:appeal_date] = Date.strptime($1, "%d %b %Y")
  elsif appeal_status =~ /^\s*This decision was appealed on (\d{1,2} \w{3} \d{4}) and decided on (\d{1,2} \w{3} \d{4})./
    record[:appeal_date] = Date.strptime($1, "%d %b %Y")
    record[:appeal_decision_date] = Date.strptime($2, "%d %b %Y")
  elsif appeal_status =~ /^\s*This decision was appealed on\s+and decided on (\d{1,2} \w{3} \d{4})./
    record[:appeal_decision_date] = Date.strptime($1, "%d %b %Y")
  else
    throw "Can't parse appeal status for #{record[:uid]}: #{appeal_status}"
  end

  if link
    appeals = agent.get(link)

    appeals.root.css("table.tablesorter > tbody > tr").each_slice(2) do |summary,details|
      columns = summary.css("td")

      if columns[1].content.strip == record[:uid]
        record[:appeal_result] = columns[5].content.strip
      end
    end
  end
end

# Process search results
def process_search_results(agent, page)
  page.root.css("table.tablesorter > tbody > tr").each_slice(2) do |summary,details|
    columns = summary.css("td")
    record = {}

    # Extract summary information
    record[:uid] = columns[1].content.strip
    record[:address] = columns[2].content.strip
    record[:description] = columns[3].content.strip
    record[:status] = columns[4].content.strip

    # Parse the details table
    details.css("table").first.css("tr").each do |row|
      columns = row.css("td")
      name = columns[0].content.strip
      value = columns[1].content.strip

      if link = columns[1].css("a").first
        link = link.attr("href")
      end

      if value.length > 0 and value != "N/A"
        case name
          when "Applicant Name"; record[:applicant_name] = value
          when "Agent Name"; record[:agent_name] = value
#          when "Delegation"; record[] = value
          when "Handling Officer"; record[:case_officer] = value
          when "Application Type"; record[:application_type] = value
#          when "Listed Building"; record[] = value
          when "Parish"; record[:parish] = value
          when "Ward"; record[:ward_name] = value
#          when "Newspaper Name"; record[] = value
          when "Publication Date"; record[:last_advertised_date] = Date.strptime(value, "%d %b %Y")
          when "Application received on"; record[:date_received] = Date.strptime(value, "%d %b %Y")
          when "Application validated on"; record[:date_validated] = Date.strptime(value, "%d %b %Y")
          when "Decision Notice"; parse_decision_notice(value, record)
          when "Appeal Status"; parse_appeal_status(value, link, record, agent)
#          when "Calculated Fee"; record[] = value
#          when "Fee Paid"; record[] = value
        end
      end
    end

    # Fill in other fields
    record[:comment_url] = "http://www.stroud.gov.uk/PLO/PlanningComments.aspx?par=#{record[:uid]}"
    record[:start_date] = [record[:date_received], record[:date_validated]].compact.min
    record[:date_scraped] = Time.now

    # Save the record
    ScraperWiki.save([:uid], record)
  end
end

# Search for planning applications in a given date range
def search_for_applications(to_date = Date.today, from_date = to_date - 60, agent = get_user_agent)
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

    # Get the search page
    search_page = agent.get("http://www.stroud.gov.uk/PLO/Default.aspx")

    # Submit the search
    search_form = search_page.form_with(:id => "form1")
    search_form.field_with(:id => "receivedafter").value = from_date.strftime("%d/%m/%Y")
    search_form.field_with(:id => "receivedb4").value = to_date.strftime("%d/%m/%Y")
    search_form.radiobutton_with(:id => "ApplicationDecided_1").check
    search_button = search_form.button_with(:id => "Button41")
    search_results = agent.submit(search_form, search_button)

    # Process the results
    process_search_results(agent, search_results)

    # Discard the page
    search_results.reset
  end
end

# Search for recent decisions
def search_for_decisions
  # Get a user agent
  agent = get_user_agent

  # Tell the user what we're doing
  log "Searching for recent decisions"

  # Get the search page
  search_page = agent.get("http://www.stroud.gov.uk/PLO/Default.aspx")

  # Submit the search
  search_form = search_page.form_with(:id => "form1")
  search_form["__EVENTTARGET"] = "ctl00$MainContent$LinkButton4"
  search_form["__EVENTARGUMENT"] = ""
  search_results = agent.submit(search_form)

  # Process the results
  process_search_results(agent, search_results)
end

search_for_applications
search_for_decisions
