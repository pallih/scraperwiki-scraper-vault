require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'https://www.jerseyfsc.org/registry/documentsearch/NameSearch.aspx'
COMPANY_TYPES = %w(RC RCO RCD RCP)
ALPHA_PLUS_DIGITS = ('A'..'Z').to_a + ('0'..'9').to_a

def next_character_to_search(prefix)
  new_prefix = prefix.dup
  final_char = new_prefix[-1]
  case final_char
  when 'Z'
    new_prefix[-1] = '0'
  when '9'
    if new_prefix.length > 1
      new_prefix[-2] = next_in_sequence(new_prefix[-2]) # get next in sequence
      new_prefix = new_prefix[0..-2] # reduce by a character
    else
      new_prefix = "A"
    end
  else
    new_prefix[-1] = final_char.succ
  end
  new_prefix
end

def next_in_sequence(char)
  ALPHA_PLUS_DIGITS[ALPHA_PLUS_DIGITS.index(char)+1]||'A'
end

# scrape_page function: gets passed an individual page to scrape
def scrape_table(page)
  rows = Nokogiri.HTML(page).css('#ContentPlaceMain_SearchResultsGridView tr')[1..-1]
  if rows.nil?
    puts "No data found"
    return true
  elsif rows.size == 300
    puts "***Too many rows to show on one page. Need to refine prefix"
    return
  end
  puts "Found #{rows.size} companies"

  rows.each do |row|
    begin
      record = {}
      company_number_link = row.at('td a') || row.at('td')
      record['CompanyNumber']   = company_number_link.inner_text.strip
      record['CompanyName']     = row.css('td')[2].inner_text.strip
      record['EntityType']      = row.css('td')[1].inner_text.strip
      record['RegistryUrl']     = "https://www.jerseyfsc.org/registry/documentsearch/NameDetail.aspx?id=" + company_number_link[:href].scan(/showDetail\(\'(\d+)/).flatten.first.to_s rescue nil
      record['date_scraped']    = Time.now
      next unless COMPANY_TYPES.include?(record['EntityType'])
      # beginning_time = Time.now
      ScraperWiki.save(["CompanyNumber"], record)
      # puts "Time elapsed #{(Time.now - beginning_time)*1000} milliseconds"
    rescue Exception => e
      puts "Exception raised while extracting data from row html: #{e.inspect}, #{row.to_html}"
    end
 end
rescue Exception => e
  puts "Exception raised while parsing data: #{e.inspect}, #{e.backtrace}"
end

def get_results_and_extract_data_for(prefix)
  sleep 2
  puts "getting companies starting with #{prefix}"
  @page.form_with(:id => 'MainForm') do |f|
    f.field_with(:name => "ctl00$ContentPlaceMain$cboType").value = "Begins With"
    f.field_with(:name => "ctl00$ContentPlaceMain$txtSearch").value = prefix
    @page = f.submit
  end
  results = scrape_table(@page.body)
  @consec_error_count = 0
  results
rescue Exception, Timeout::Error => e
  @consec_error_count += 1
  puts "xxxxxx An error occured (happened #{@consec_error_count} times, sleeping now for #{(30 * @consec_error_count)} seconds): #{e.inspect}#{e.backtrace} (happened #{@consec_error_count} times)"
  sleep (30 * @consec_error_count)
  exit if @consec_error_count > 4
  @refetch_start_page = true
  get_results_and_extract_data_for(prefix)
end


# ---------------------------------------------------------------------------
# SCRIPT ACTION STARTS HERE
# ---------------------------------------------------------------------------

@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
  browser.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
# get first page to pick up cookies etc
@page = @br.get(BASE_URL)

prefix = ScraperWiki.get_var('prefix', 'A')
@consec_error_count = 0

loop do
  ScraperWiki.save_var('prefix', prefix) # save prefix for when scraper gets killed
  results = get_results_and_extract_data_for(prefix)
  if !results
    prefix += "A"
  else
    prefix = next_character_to_search(prefix)
  end
end
