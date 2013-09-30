require 'rubygems'
require 'hpricot'
require 'date'
require 'net/https'
require 'json'
require 'open-uri'

host = "esd.cttt.nsw.gov.au"
url = "/Hearing/HearingList.aspx?LocationCode="

# The certificate was failing so we need to do this jiggery pokery
http = Net::HTTP.new(host, 443)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

# Get the list of venues from the venue scraper
venue_list = JSON.parse(open("http://api.scraperwiki.com/api/1.0/datastore/getdata?format=json&name=cttt-hearing-venues").read)

venue_list.each do |v|
  venue_url = url + v["postcode"]

  begin
    response = http.get(venue_url)
  rescue Timeout::Error
    puts "Timed out on #{venue_url}. Skipping."
    next
  end

  page = Hpricot(response.body)
  
  # This way of working out the dates probably won't last
  # need to work out when the data is posted, etc.
  (Date.today..Date.today + 30).each do |d|
    puts "Processing #{d} for #{v['postcode']}"
    id = '//*[@id="dg' + d.strftime("%-d%-m%Y") + '"]'
    (page/id).each do |r|
      # First get room and time. The format is different for the first
      # result
      if r.previous.previous.search('b')[1].nil?
        time_and_place = r.previous.previous.inner_text
      else
        time_and_place = r.previous.previous.search('b')[1].inner_text
      end
    
      # Now the cases
      r.search('tr.clsGridItem').each do |c|
        cttt_case = {
          'unique_id'           => (d.to_s + c.search('td')[0].inner_text).split.join,
          'case_number'         => c.search('td')[0].inner_text,
          'party_a'             => c.search('td')[1].inner_text,
          'party_b'             => c.search('td')[2].inner_text,
          'date'                => d.to_s,
          'time'                => time_and_place.split(" at ", 2)[0],
          'location'            => time_and_place.split(" at ", 2)[1].strip,
          'venue'               => v["location"],
          'venue_postcode'      => v["postcode"]
        }
    
        ScraperWiki.save(['unique_id'], cttt_case)
      end
    end
  end
endrequire 'rubygems'
require 'hpricot'
require 'date'
require 'net/https'
require 'json'
require 'open-uri'

host = "esd.cttt.nsw.gov.au"
url = "/Hearing/HearingList.aspx?LocationCode="

# The certificate was failing so we need to do this jiggery pokery
http = Net::HTTP.new(host, 443)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

# Get the list of venues from the venue scraper
venue_list = JSON.parse(open("http://api.scraperwiki.com/api/1.0/datastore/getdata?format=json&name=cttt-hearing-venues").read)

venue_list.each do |v|
  venue_url = url + v["postcode"]

  begin
    response = http.get(venue_url)
  rescue Timeout::Error
    puts "Timed out on #{venue_url}. Skipping."
    next
  end

  page = Hpricot(response.body)
  
  # This way of working out the dates probably won't last
  # need to work out when the data is posted, etc.
  (Date.today..Date.today + 30).each do |d|
    puts "Processing #{d} for #{v['postcode']}"
    id = '//*[@id="dg' + d.strftime("%-d%-m%Y") + '"]'
    (page/id).each do |r|
      # First get room and time. The format is different for the first
      # result
      if r.previous.previous.search('b')[1].nil?
        time_and_place = r.previous.previous.inner_text
      else
        time_and_place = r.previous.previous.search('b')[1].inner_text
      end
    
      # Now the cases
      r.search('tr.clsGridItem').each do |c|
        cttt_case = {
          'unique_id'           => (d.to_s + c.search('td')[0].inner_text).split.join,
          'case_number'         => c.search('td')[0].inner_text,
          'party_a'             => c.search('td')[1].inner_text,
          'party_b'             => c.search('td')[2].inner_text,
          'date'                => d.to_s,
          'time'                => time_and_place.split(" at ", 2)[0],
          'location'            => time_and_place.split(" at ", 2)[1].strip,
          'venue'               => v["location"],
          'venue_postcode'      => v["postcode"]
        }
    
        ScraperWiki.save(['unique_id'], cttt_case)
      end
    end
  end
end