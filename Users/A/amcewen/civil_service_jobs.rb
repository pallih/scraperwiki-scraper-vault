# Ruby scraper for http://www.civilservice.gov.uk/jobs/ jobs
require 'nokogiri'
require 'uri'

# Name of the database table where the results are stored
DB_NAME = 'civil_service_jobs'

@record_count = 0

# retrieve the news index page
base_url = "http://www.civilservice.gov.uk/jobs/Job-search-results.aspx"
starting_url = base_url

# Function to try to map an address to a lat/lng using Geonames
# Takes an address string and return an array of [lat, lng] or nil if the address couldn't be mapped
def gb_address_to_latlng(address)
  encoded_address = CGI.escape(address)
  result = ScraperWiki.scrape("http://api.geonames.org/search?q=#{encoded_address}&country=gb&username=amcewen&maxRows=1")
  result_doc = Nokogiri::HTML(result)
  unless result_doc.css("geoname").empty? 
    return [result_doc.css("geoname lat").inner_text, result_doc.css("geoname lng").inner_text]
  else
    # We seem to get addresses like "Lowestoft, Suffolk, South East" and Geonames doesn't like
    # the "South East" part, so try removing the last clause
    addr_clauses = address.split(',')
    if addr_clauses.size > 1
      addr_clauses.delete_at(addr_clauses.size-1)
      return gb_address_to_latlng(addr_clauses.join(", "))
    else
      return nil
    end
  end
end

def record_job_details(job_url)
  @record_count = @record_count + 1
  puts "#{@record_count} Recording job #{job_url}"

  record = { 'URI' => job_url }

  job_html = ScraperWiki.scrape(job_url)
 
  job = Nokogiri::HTML(job_html)

  record['title'] = job.css('h2[property="dc:title"]').inner_text.strip
  record['reference'] = job.css('span[property="dc:identifier"]').inner_text.strip
  record['working_arrangement'] = job.css('p[property="arg:workingArrangements"]').inner_text.strip
  record['employer'] = job.css("#JobDetails1_theJobInfo_ctl01_departmentName").inner_text.strip
  record['post_date'] = Date.parse(job.css('meta[name="DC.date.issued"]')[0]['content']).to_s

  salaryFrom = job.css('span[property="arg:salaryFrom"]')
  salaryTo = job.css('span[property="arg:salaryTo"]')
  unless salaryFrom.empty? 
    record['pay'] = salaryFrom[0]['content']
    unless salaryTo.empty? 
      record['pay'] = record['pay']+" - "+salaryTo[0]['content']
    end
  else
    unless job.css('span[property="arg:salary"]').empty? 
      record['pay'] = job.css('span[property="arg:salary"]')[0]['content']
    else
      raise "#### ERROR: Couldn't find salary details"
    end
  end

  description = []
  node = job.css('p[property="dc:description"]')[0]
  while node.name == 'p' || node.name == 'text' do
    description.push(node)
    node = node.next_sibling
  end
  record['description'] = description.collect { |n| n.to_s }.join

  apply = []
  job.css("h2.underline").each do |h|
    if h.inner_text.match(/how to apply/i)
      # This is the "How to Apply" section, extract all the paragraphs in it
      node = h.next
      while node.name == 'p' || node.name == 'text' do
        apply.push(node)
        node = node.next_sibling
      end
    end
  end
  record['how_to_apply'] = apply.collect { |n| n.to_s }.join("\n")

  record['location'] = job.css('p[property="dc:coverage"]').inner_text
  # regexp acquired from "Zefram" via "osfameron" on IRC.
  # Derived from http://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation
  postcode = record['location'].match(/[A-PR-UWYZa-pr-uwyz]([0-9][0-9A-HJKS-UWa-hjks-uw]?|[A-HK-Ya-hk-y][0-9][0-9ABEHMNPRV-Yabehmnprv-y]?) +[0-9][ABD-HJLNP-UW-Zabd-hjlnp-uw-z]{2}|[Gg][Ii][Rr] +0[Aa][Aa]|[Ss][Aa][Nn] +[Tt][Aa]1/)
  unless postcode.nil? 
    record['postcode'] = postcode[0]
    coords = ScraperWiki.gb_postcode_to_latlng(record['postcode'])
    record['lat'] = coords[0]
    record['lng'] = coords[1]

    ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
  else
    coords = gb_address_to_latlng(record['location'].gsub(/\(.*\)/, ""))
    unless coords.nil? 
      record['lat'] = coords[0]
      record['lng'] = coords[1]

      ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
    else
      puts "Failed to find lat/lng for "+job.css('p[property="dc:coverage"]').inner_text
    end
  end
end

# Keep getting pages of results until we reach the end (i.e. a page without a "Next" link)
while !starting_url.nil? 
  puts "Getting "+starting_url
  parsed_base_url = URI.parse(starting_url)
  html = ScraperWiki.scrape(starting_url)
 
  doc = Nokogiri::HTML(html)

  # Find all the results on this page
  doc.css("table.results caption a").each do |job_link|
    job_permalink = parsed_base_url.merge(job_link['href']).to_s
    # See if we've already got this job, and if not then retrieve it
    begin
      if ScraperWiki.select("* from '#{DB_NAME}' where URI = '#{job_permalink}'").empty? 
        record_job_details(job_permalink)
      else
        puts "Already got job #{job_permalink}"
      end
    rescue
      # FIXME Ideally just catch the error when there's no database and let other errors alert user
      record_job_details(job_permalink)
    end
  end

  # Get the next page of results
  last_page_link = doc.css("#JobListing1_PaginationControl_dvpagination a").last
  if last_page_link.inner_text.match(/next/i).nil? 
    # We've reached the end of the results
    starting_url = nil
  else
    # Get the next page of results
    starting_url = parsed_base_url.merge(last_page_link['href']).to_s
  end
end

# Ruby scraper for http://www.civilservice.gov.uk/jobs/ jobs
require 'nokogiri'
require 'uri'

# Name of the database table where the results are stored
DB_NAME = 'civil_service_jobs'

@record_count = 0

# retrieve the news index page
base_url = "http://www.civilservice.gov.uk/jobs/Job-search-results.aspx"
starting_url = base_url

# Function to try to map an address to a lat/lng using Geonames
# Takes an address string and return an array of [lat, lng] or nil if the address couldn't be mapped
def gb_address_to_latlng(address)
  encoded_address = CGI.escape(address)
  result = ScraperWiki.scrape("http://api.geonames.org/search?q=#{encoded_address}&country=gb&username=amcewen&maxRows=1")
  result_doc = Nokogiri::HTML(result)
  unless result_doc.css("geoname").empty? 
    return [result_doc.css("geoname lat").inner_text, result_doc.css("geoname lng").inner_text]
  else
    # We seem to get addresses like "Lowestoft, Suffolk, South East" and Geonames doesn't like
    # the "South East" part, so try removing the last clause
    addr_clauses = address.split(',')
    if addr_clauses.size > 1
      addr_clauses.delete_at(addr_clauses.size-1)
      return gb_address_to_latlng(addr_clauses.join(", "))
    else
      return nil
    end
  end
end

def record_job_details(job_url)
  @record_count = @record_count + 1
  puts "#{@record_count} Recording job #{job_url}"

  record = { 'URI' => job_url }

  job_html = ScraperWiki.scrape(job_url)
 
  job = Nokogiri::HTML(job_html)

  record['title'] = job.css('h2[property="dc:title"]').inner_text.strip
  record['reference'] = job.css('span[property="dc:identifier"]').inner_text.strip
  record['working_arrangement'] = job.css('p[property="arg:workingArrangements"]').inner_text.strip
  record['employer'] = job.css("#JobDetails1_theJobInfo_ctl01_departmentName").inner_text.strip
  record['post_date'] = Date.parse(job.css('meta[name="DC.date.issued"]')[0]['content']).to_s

  salaryFrom = job.css('span[property="arg:salaryFrom"]')
  salaryTo = job.css('span[property="arg:salaryTo"]')
  unless salaryFrom.empty? 
    record['pay'] = salaryFrom[0]['content']
    unless salaryTo.empty? 
      record['pay'] = record['pay']+" - "+salaryTo[0]['content']
    end
  else
    unless job.css('span[property="arg:salary"]').empty? 
      record['pay'] = job.css('span[property="arg:salary"]')[0]['content']
    else
      raise "#### ERROR: Couldn't find salary details"
    end
  end

  description = []
  node = job.css('p[property="dc:description"]')[0]
  while node.name == 'p' || node.name == 'text' do
    description.push(node)
    node = node.next_sibling
  end
  record['description'] = description.collect { |n| n.to_s }.join

  apply = []
  job.css("h2.underline").each do |h|
    if h.inner_text.match(/how to apply/i)
      # This is the "How to Apply" section, extract all the paragraphs in it
      node = h.next
      while node.name == 'p' || node.name == 'text' do
        apply.push(node)
        node = node.next_sibling
      end
    end
  end
  record['how_to_apply'] = apply.collect { |n| n.to_s }.join("\n")

  record['location'] = job.css('p[property="dc:coverage"]').inner_text
  # regexp acquired from "Zefram" via "osfameron" on IRC.
  # Derived from http://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation
  postcode = record['location'].match(/[A-PR-UWYZa-pr-uwyz]([0-9][0-9A-HJKS-UWa-hjks-uw]?|[A-HK-Ya-hk-y][0-9][0-9ABEHMNPRV-Yabehmnprv-y]?) +[0-9][ABD-HJLNP-UW-Zabd-hjlnp-uw-z]{2}|[Gg][Ii][Rr] +0[Aa][Aa]|[Ss][Aa][Nn] +[Tt][Aa]1/)
  unless postcode.nil? 
    record['postcode'] = postcode[0]
    coords = ScraperWiki.gb_postcode_to_latlng(record['postcode'])
    record['lat'] = coords[0]
    record['lng'] = coords[1]

    ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
  else
    coords = gb_address_to_latlng(record['location'].gsub(/\(.*\)/, ""))
    unless coords.nil? 
      record['lat'] = coords[0]
      record['lng'] = coords[1]

      ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
    else
      puts "Failed to find lat/lng for "+job.css('p[property="dc:coverage"]').inner_text
    end
  end
end

# Keep getting pages of results until we reach the end (i.e. a page without a "Next" link)
while !starting_url.nil? 
  puts "Getting "+starting_url
  parsed_base_url = URI.parse(starting_url)
  html = ScraperWiki.scrape(starting_url)
 
  doc = Nokogiri::HTML(html)

  # Find all the results on this page
  doc.css("table.results caption a").each do |job_link|
    job_permalink = parsed_base_url.merge(job_link['href']).to_s
    # See if we've already got this job, and if not then retrieve it
    begin
      if ScraperWiki.select("* from '#{DB_NAME}' where URI = '#{job_permalink}'").empty? 
        record_job_details(job_permalink)
      else
        puts "Already got job #{job_permalink}"
      end
    rescue
      # FIXME Ideally just catch the error when there's no database and let other errors alert user
      record_job_details(job_permalink)
    end
  end

  # Get the next page of results
  last_page_link = doc.css("#JobListing1_PaginationControl_dvpagination a").last
  if last_page_link.inner_text.match(/next/i).nil? 
    # We've reached the end of the results
    starting_url = nil
  else
    # Get the next page of results
    starting_url = parsed_base_url.merge(last_page_link['href']).to_s
  end
end

