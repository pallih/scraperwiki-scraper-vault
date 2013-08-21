# Ruby scraper for http://jobseekers.direct.gov.uk/ jobs
require 'nokogiri'
require 'uri'
require 'mechanize'

# This scraper will deal with all the postcodes beginning with these letters
POSTCODE_PREFIXES = ["H", "I", "J", "K"]

Mechanize.html_parser = Nokogiri::HTML

# Name of the database table where the results are stored
DB_NAME = 'jobseekers_jobs'

@record_count = 0

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

def record_job_details(job_link, full_or_part_time)
  @record_count = @record_count + 1
  puts "#{@record_count} Recording job "+job_link

  record = { 'URI' => job_link.gsub(/sessionid=[\d\w-]+/, ""), 'working_arrangement' => full_or_part_time }
  job_page = @br.get(@parsed_home_url.merge(job_link).to_s)
  job = Nokogiri::HTML(job_page.body)

  record['title'] = job.css('#hdgJobTitle').inner_text.strip
  record['reference'] = job.css('#parJobNo').inner_text.strip
  record['employer'] = job.css("#parEmployerName").inner_text.strip
  record['post_date'] = Date.parse(job.css('#parDatePosted').inner_text).to_s
  record['pay'] = job.css('#parWage').inner_text.strip
  record['description'] = job.css('#parDescription').to_s
  record['how_to_apply'] = job.css('#parHowToApply').to_s
  record['location'] = job.css('#parLocation').inner_text
  coords = gb_address_to_latlng(record['location'])
  if coords.nil? 
    # Couldn't map address, but quite a few have a trailing first-half postcode which
    # throws Geonames, so try without that
    coords = gb_address_to_latlng(record['location'].gsub(/\w\w?\d\d?\w?$/, "").strip)
  end

  unless coords.nil? 
    record['lat'] = coords[0]
     record['lng'] = coords[1]
  else
    puts "Failed to map "+record['location']
  end
  ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
end

def scrape_jobs(page_body, full_or_part_time)
  doc = Nokogiri::HTML(page_body, nil, 'utf-8')
  doc.css("td.JobTitle a").each do |job_link|
    # See if we've already got this job, and if not then retrieve it
    begin
      job_key = job_link['href'].gsub(/sessionid=[\d\w-]+/, "")
      if ScraperWiki.select("* from '#{DB_NAME}' where URI = '#{job_key}'").empty? 
        record_job_details(job_link['href'], full_or_part_time)
      else
        puts "Already got job #{job_key}"
      end
    rescue
      # FIXME Ideally just catch the error when there's no database and let other errors alert user
      record_job_details(job_link['href'], full_or_part_time)
    end
  end
end

def scrape_and_look_for_next_link(initial_page, full_or_part_time)
  # Record all the jobs on this page
  scrape_jobs(initial_page.body, full_or_part_time)

  # See if there are any more results to check through
  link = initial_page.link_with(:text => 'Next page')
  if link
    next_page = @br.get(@parsed_home_url.merge(link.href).to_s)
    scrape_and_look_for_next_link(next_page, full_or_part_time)
  end
end

# The jobseekers website is annoying because it insists on redirecting you to the homepage whenever you
# visit for the first time, so we have to navigate through to the page that we're interested in...
# (it also means that none of the job URLs will be reusable, *sigh*)
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}

home_url = "http://jobseekers.direct.gov.uk/homepage.aspx"
@parsed_home_url = URI.parse(home_url)

counts = {}
ScraperWiki.attach('uk_postcode_districts') 
ScraperWiki.select('* from `uk_postcode_districts`').each do |district|
  if POSTCODE_PREFIXES.include?(district['postcode_district'][0,1])
    (0..9).each do |num|
      puts "Searching "+district['postcode_district']+" #{num}"
      # Run through this three times, the first two are for part-time jobs (hours < 30) and the third is full-time
      full_or_part_time = { "30" => "Part time", "40" => "Part time", "60" => "Full time" }
      ["30", "40", "60"].each do |hours|
        puts "Hours: "+full_or_part_time[hours]
        begin
          search_page = @br.get(home_url)
          search_page.form_with(:name => 'Homepage') do |f|
            f['txtSubject'] = "all jobs"
            f['txtLocation'] = district['postcode_district']+" #{num}"
            f['ddlDistance'] = "3" # jobs within 5 miles
            f['ddlAge'] = "1" # "today's jobs"
            f['ddlHours'] = hours
            f['btnSearch'] = "Search"
            results = f.submit()
            scrape_and_look_for_next_link(results, full_or_part_time[hours])
          end
        rescue Timeout::Error
          puts "Requests timed out, carrying on with the next search"
          # Create a new browser object because it seems to be left in a strange state otherwise
          @br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
            browser.user_agent_alias = 'Linux Firefox'
          }
        end
      end
    end
  end
end

