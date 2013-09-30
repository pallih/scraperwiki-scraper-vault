#!/usr/bin/env ruby

# Revised scraper for Multnomah County Sheriff's Office Online Inmate Data
# (http://www.mcso.us/PAID/)
# Output is now JSON, with nesting structure defined by website as of
# 2013-05-10. Just about every database and programming language out in the
# wild can deal with JSON, and a trivial two-pass algorithm can convert it
# to CSV if necessary.

require 'scraperwiki'
require 'nokogiri'
require 'open-uri'
require 'mechanize'
require 'json'

# constant definitions
UNIQUE_KEYS = [ 'booking_number' ]
SEARCH_URL = "http://www.mcso.us/PAID"
BOOKING_URL = "http://www.mcso.us"
MUGSHOT_URL = "http://www.mcso.us/PAID/Home/MugshotImage"
SEARCH_TYPES = [
  'Now in Custody',
  'Released Last 7 Days',
  'Emergency Releases Last 7 Day',
  'Booked Last 7 Days'
]

# conversion from MCSO labels to SNAKE_CASE
SNAKE_CASE = Hash.new
SNAKE_CASE['Person_SwisID'] = 'person_swis_id'
SNAKE_CASE['Person_FullName'] = 'person_full_name'
SNAKE_CASE['Person_Age'] = 'person_age'
SNAKE_CASE['Person_Gender'] = 'person_gender'
SNAKE_CASE['Person_Race'] = 'person_race'
SNAKE_CASE['Person_Height'] = 'person_height'
SNAKE_CASE['Person_Weight'] = 'person_weight'
SNAKE_CASE['Person_HairColor'] = 'person_hair_color'
SNAKE_CASE['Person_EyeColor'] = 'person_eye_color'
SNAKE_CASE['ArrestingAgency'] = 'arresting_agency'
SNAKE_CASE['ArrestDateTime'] = 'arrest_date_time'
SNAKE_CASE['BookingDateTime'] = 'booking_date_time'
SNAKE_CASE['CurrentStatus'] = 'current_status'
SNAKE_CASE['AssignedFacility'] = 'assigned_facility'
SNAKE_CASE['ProjectedReleaseDateTime'] = 'projected_release_date_time'
SNAKE_CASE['ReleaseDateTime'] = 'release_date_time'
SNAKE_CASE['ReleaseReason'] = 'release_reason'

# method to get a booking page
def get_booking_page(link, search_type)

  # initialize the output hash
  booking_detail_hash = Hash.new
  booking_detail_hash['booking_number'] = link.href.split('/').pop
  booking_detail_hash['link'] = BOOKING_URL + link.href
  booking_detail_hash['search_type'] = SEARCH_TYPES[search_type]
  booking_detail_hash['mugshot_link'] = MUGSHOT_URL + '/' + 
    booking_detail_hash['booking_number']

  # get the page - need to retry sometimes
  page = ''
  while page == ''
    begin
      page = Nokogiri::HTML(open(BOOKING_URL + link.href))
    rescue Exception
      puts "\{\"failed_link\":\"#{link.href}\",\"message\":\"#{$!.to_json}\"\}"
      STDOUT.flush
    end
  end
  
  # get booking record
  article = page.css("article").inner_html
  previous_line = ''
  label = ''
  article.lines.each do |line|
    if line =~ /label for=/
      label = line.chomp.sub(/^.*label for="/, '').sub(/".*$/, '')
    elsif previous_line =~ /display-value/
      value = line.chomp.sub(/^[ \t]*/, '')
      booking_detail_hash[SNAKE_CASE[label]] = value
    end
    previous_line = line
  end
  
  # now collect court cases and charges
  court_cases_array = Array.new
  court_case_hash = Hash.new
  charges_array = Array.new
  charge_hash = Hash.new
  
  court_cases_html = page.css('#charge-info').inner_html
  court_cases_html.lines.each do |line|
    if line =~ /court-case-number/ # beginning of a court case
      court_case_hash = Hash.new
      court_case_hash['court_case_number'] = line.chomp.sub(/^.*<b>/, '').sub(/<\/b>.*$/, '')
    elsif line =~ /da-case-number/
      court_case_hash['da_case_number'] = line.chomp.sub(/^.*<b>/, '').sub(/<\/b>.*$/, '')
    elsif line =~ /citation-number/
      court_case_hash['citation_number'] = line.chomp.sub(/^.*<b>/, '').sub(/<\/b>.*$/, '')
      charges_array = Array.new
    elsif line =~ /charge-description-display/ # beginning of a list of charges
      charge_hash = Hash.new
      charge_hash['charge_description_display'] = line.chomp.sub(/^.*charge-description-display">/, '').sub(/<.*$/, '')
    elsif line =~ /charge-bail-value/
      charge_hash['charge_bail_value'] = line.chomp.sub(/^.*charge-bail-value">/, '').sub(/<.*$/, '')
    elsif line =~ /charge-status-value/
      charge_hash['charge_status_value'] = line.chomp.sub(/^.*charge-status-value">/, '').sub(/<.*$/, '')
      charges_array.push(charge_hash) # last line of a charge
    elsif line =~ /<\/ol>/ # we have all the charges for this court case!
      court_case_hash['charges_array'] = charges_array
      court_cases_array.push(court_case_hash)
    end
  end
  
  # now we have all court cases for this booking record
  booking_detail_hash['court_cases_array'] = court_cases_array
  return booking_detail_hash
end

# method to submit the search form
def submit_search_form(agent, search_type)
  agent.history.clear
  page = agent.get(SEARCH_URL)
  page.forms.first['SearchType'] = search_type
  search_results = page.forms.first.click_button()
  search_results.links.each do |link|
    link_text = link.href.to_s
    next if link_text !~ /PAID\/Home\/Booking/ # only care about links to BookingDetail

    # get the booking page
    booking_detail_hash = get_booking_page(link, search_type)

    # send to outputs
    #puts booking_detail_hash.to_json
    #STDOUT.flush
    temp = booking_detail_hash['court_cases_array']
    booking_detail_hash['court_cases_array'] = temp.to_json
    ScraperWiki.save_sqlite(UNIQUE_KEYS, booking_detail_hash)
  end
end

# Main program

# Create an agent
agent = Mechanize.new { |browser| browser.user_agent_alias = 'Linux Firefox' }

submit_search_form(agent, 3) # Booked Last 7 Days
submit_search_form(agent, 2) # Emergency Releases Last 7 Days
submit_search_form(agent, 1) # Released Last 7 Days
submit_search_form(agent, 0) # Now in Custody

#!/usr/bin/env ruby

# Revised scraper for Multnomah County Sheriff's Office Online Inmate Data
# (http://www.mcso.us/PAID/)
# Output is now JSON, with nesting structure defined by website as of
# 2013-05-10. Just about every database and programming language out in the
# wild can deal with JSON, and a trivial two-pass algorithm can convert it
# to CSV if necessary.

require 'scraperwiki'
require 'nokogiri'
require 'open-uri'
require 'mechanize'
require 'json'

# constant definitions
UNIQUE_KEYS = [ 'booking_number' ]
SEARCH_URL = "http://www.mcso.us/PAID"
BOOKING_URL = "http://www.mcso.us"
MUGSHOT_URL = "http://www.mcso.us/PAID/Home/MugshotImage"
SEARCH_TYPES = [
  'Now in Custody',
  'Released Last 7 Days',
  'Emergency Releases Last 7 Day',
  'Booked Last 7 Days'
]

# conversion from MCSO labels to SNAKE_CASE
SNAKE_CASE = Hash.new
SNAKE_CASE['Person_SwisID'] = 'person_swis_id'
SNAKE_CASE['Person_FullName'] = 'person_full_name'
SNAKE_CASE['Person_Age'] = 'person_age'
SNAKE_CASE['Person_Gender'] = 'person_gender'
SNAKE_CASE['Person_Race'] = 'person_race'
SNAKE_CASE['Person_Height'] = 'person_height'
SNAKE_CASE['Person_Weight'] = 'person_weight'
SNAKE_CASE['Person_HairColor'] = 'person_hair_color'
SNAKE_CASE['Person_EyeColor'] = 'person_eye_color'
SNAKE_CASE['ArrestingAgency'] = 'arresting_agency'
SNAKE_CASE['ArrestDateTime'] = 'arrest_date_time'
SNAKE_CASE['BookingDateTime'] = 'booking_date_time'
SNAKE_CASE['CurrentStatus'] = 'current_status'
SNAKE_CASE['AssignedFacility'] = 'assigned_facility'
SNAKE_CASE['ProjectedReleaseDateTime'] = 'projected_release_date_time'
SNAKE_CASE['ReleaseDateTime'] = 'release_date_time'
SNAKE_CASE['ReleaseReason'] = 'release_reason'

# method to get a booking page
def get_booking_page(link, search_type)

  # initialize the output hash
  booking_detail_hash = Hash.new
  booking_detail_hash['booking_number'] = link.href.split('/').pop
  booking_detail_hash['link'] = BOOKING_URL + link.href
  booking_detail_hash['search_type'] = SEARCH_TYPES[search_type]
  booking_detail_hash['mugshot_link'] = MUGSHOT_URL + '/' + 
    booking_detail_hash['booking_number']

  # get the page - need to retry sometimes
  page = ''
  while page == ''
    begin
      page = Nokogiri::HTML(open(BOOKING_URL + link.href))
    rescue Exception
      puts "\{\"failed_link\":\"#{link.href}\",\"message\":\"#{$!.to_json}\"\}"
      STDOUT.flush
    end
  end
  
  # get booking record
  article = page.css("article").inner_html
  previous_line = ''
  label = ''
  article.lines.each do |line|
    if line =~ /label for=/
      label = line.chomp.sub(/^.*label for="/, '').sub(/".*$/, '')
    elsif previous_line =~ /display-value/
      value = line.chomp.sub(/^[ \t]*/, '')
      booking_detail_hash[SNAKE_CASE[label]] = value
    end
    previous_line = line
  end
  
  # now collect court cases and charges
  court_cases_array = Array.new
  court_case_hash = Hash.new
  charges_array = Array.new
  charge_hash = Hash.new
  
  court_cases_html = page.css('#charge-info').inner_html
  court_cases_html.lines.each do |line|
    if line =~ /court-case-number/ # beginning of a court case
      court_case_hash = Hash.new
      court_case_hash['court_case_number'] = line.chomp.sub(/^.*<b>/, '').sub(/<\/b>.*$/, '')
    elsif line =~ /da-case-number/
      court_case_hash['da_case_number'] = line.chomp.sub(/^.*<b>/, '').sub(/<\/b>.*$/, '')
    elsif line =~ /citation-number/
      court_case_hash['citation_number'] = line.chomp.sub(/^.*<b>/, '').sub(/<\/b>.*$/, '')
      charges_array = Array.new
    elsif line =~ /charge-description-display/ # beginning of a list of charges
      charge_hash = Hash.new
      charge_hash['charge_description_display'] = line.chomp.sub(/^.*charge-description-display">/, '').sub(/<.*$/, '')
    elsif line =~ /charge-bail-value/
      charge_hash['charge_bail_value'] = line.chomp.sub(/^.*charge-bail-value">/, '').sub(/<.*$/, '')
    elsif line =~ /charge-status-value/
      charge_hash['charge_status_value'] = line.chomp.sub(/^.*charge-status-value">/, '').sub(/<.*$/, '')
      charges_array.push(charge_hash) # last line of a charge
    elsif line =~ /<\/ol>/ # we have all the charges for this court case!
      court_case_hash['charges_array'] = charges_array
      court_cases_array.push(court_case_hash)
    end
  end
  
  # now we have all court cases for this booking record
  booking_detail_hash['court_cases_array'] = court_cases_array
  return booking_detail_hash
end

# method to submit the search form
def submit_search_form(agent, search_type)
  agent.history.clear
  page = agent.get(SEARCH_URL)
  page.forms.first['SearchType'] = search_type
  search_results = page.forms.first.click_button()
  search_results.links.each do |link|
    link_text = link.href.to_s
    next if link_text !~ /PAID\/Home\/Booking/ # only care about links to BookingDetail

    # get the booking page
    booking_detail_hash = get_booking_page(link, search_type)

    # send to outputs
    #puts booking_detail_hash.to_json
    #STDOUT.flush
    temp = booking_detail_hash['court_cases_array']
    booking_detail_hash['court_cases_array'] = temp.to_json
    ScraperWiki.save_sqlite(UNIQUE_KEYS, booking_detail_hash)
  end
end

# Main program

# Create an agent
agent = Mechanize.new { |browser| browser.user_agent_alias = 'Linux Firefox' }

submit_search_form(agent, 3) # Booked Last 7 Days
submit_search_form(agent, 2) # Emergency Releases Last 7 Days
submit_search_form(agent, 1) # Released Last 7 Days
submit_search_form(agent, 0) # Now in Custody

