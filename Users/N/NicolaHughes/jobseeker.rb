# Ruby scraper for http://jobseekers.direct.gov.uk/ jobs
require 'nokogiri'
require 'uri'
require 'mechanize'

# run details
require "date"
today = Date.today
week = today.cweek
year =  today.year

start_town = nil

begin
  setup = ScraperWiki.sqliteexecute("select * from jobstate where year=#{year} and week=#{week}")    
rescue
  ScraperWiki.save_sqlite( ['week','year'], { 'week'=>week, 'year'=>year }, table_name='jobstate')
  setup = ScraperWiki.sqliteexecute("select * from jobstate where year=#{year} and week=#{week}")    
end

if setup['keys'].include?('town')
  start_town = setup['data'][0][2]
else 
  pp setup
end


# This scraper will deal with all the postcodes beginning with these letters
#POSTCODE_PREFIXES = ["N", "O"]

Mechanize.html_parser = Nokogiri::HTML

# Name of the database table where the results are stored
DB_NAME = 'jobseekers_jobs'

@record_count = 0


def record_job_details(job_link, full_or_part_time, search_town, lat, lng)
  @record_count = @record_count + 1
  puts " #{@record_count} Recording job "+job_link

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
  record['searchtown'] = search_town
  record['lat'] = lat
  record['lng'] = lng
  ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
end

def scrape_jobs(page_body, full_or_part_time, search_town, lat, lng)
  doc = Nokogiri::HTML(page_body, nil, 'utf-8')
  doc.css("td.JobTitle a").each do |job_link|
    # See if we've already got this job, and if not then retrieve it
    begin
      job_key = job_link['href'].gsub(/sessionid=[\d\w-]+/, "")
      if ScraperWiki.select("* from '#{DB_NAME}' where URI = '#{job_key}'").empty? 
        record_job_details(job_link['href'], full_or_part_time, search_town, lat, lng)
      else
        puts " Already got job #{job_key}"
      end
    rescue
      # FIXME Ideally just catch the error when there's no database and let other errors alert user
      record_job_details(job_link['href'], full_or_part_time, search_town, lat, lng)
    end
  end
end

def scrape_and_look_for_next_link(initial_page, full_or_part_time,search_town, lat, lng)
  # Record all the jobs on this page
  scrape_jobs(initial_page.body, full_or_part_time,search_town, lat, lng )

  # See if there are any more results to check through
  link = initial_page.link_with(:text => 'Next page')
  if link
    next_page = @br.get(@parsed_home_url.merge(link.href).to_s)
    scrape_and_look_for_next_link(next_page, full_or_part_time,search_town, lat, lng)
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
ScraperWiki.attach('uktowns') 
ScraperWiki.select('town,lat,lng from `towns` order by town').each do |district|
      if start_town != nil
        puts start_town
        if district['town'] != start_town
          puts "************** Skipping " + district['town']
          next
        else
          start_town = nil
          next
        end
      end
      puts "Searching "+ district['town']
      puts "******************************************"
      # Run through this three times, the first two are for part-time jobs (hours < 30) and the third is full-time
      full_or_part_time = { "30" => "Part time", "40" => "Part time", "60" => "Full time" }
      ["30", "40", "60"].each do |hours|
        puts " Hours: "+full_or_part_time[hours]
        begin
          search_page = @br.get(home_url)
          search_page.form_with(:name => 'Homepage') do |f|
            f['txtSubject'] = "all jobs"
            f['txtLocation'] = district['town']
            f['ddlDistance'] = "4" # jobs within 15 miles
            f['ddlAge'] = "1" # "today's jobs"
            f['ddlHours'] = hours
            f['btnSearch'] = "Search"
            results = f.submit()
            scrape_and_look_for_next_link(results, full_or_part_time[hours],district['town'],district['lat'],district['lng'])
          end
        rescue Timeout::Error
          puts " Requests timed out, carrying on with the next search"
          # Create a new browser object because it seems to be left in a strange state otherwise
          @br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
            browser.user_agent_alias = 'Linux Firefox'
          }
        end

        ScraperWiki.save_sqlite( ['week','year'], { 'week'=>week, 'year'=>year, 'town'=>district['town'] }, table_name='jobstate')
      end
end

