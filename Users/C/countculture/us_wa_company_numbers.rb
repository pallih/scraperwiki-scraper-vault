require 'rubygems'
require 'nokogiri'
require 'net/http'
require 'json'

ALPHA_PLUS_DIGITS = ("A".."Z").to_a + ("0".."9").to_a
POSSIBLE_PREFIXES = ALPHA_PLUS_DIGITS.map{|l| ALPHA_PLUS_DIGITS.map{|l2| l+l2}}.flatten

#ScraperWiki.sqliteexecute("DELETE from swdata where CompanyNumber LIKE '[%'")
#ScraperWiki.sqliteexecute('create INDEX date_scraped_index on swdata (date_scraped);')

#exit

# scrape_page function: gets passed an individual page to scrape
def scrape_page(page)
  page.css('ul.CorpsListItems li a').collect do |link|
    record = {'CompanyName'  => link.content.strip,
              'CompanyNumber'=> link[:onclick].scan(/\d+/).first.to_s,
              'RetrievedAt' => Time.now
             }
    next if record['CompanyNumber'].nil? || record['CompanyNumber'] == '' 
    ScraperWiki.save(["CompanyNumber"], record)
  end
rescue Exception => e
  puts "Exception raised while getting or parsing data: #{e.inspect}"
end
        
def get_results_and_extract_data_for(letters)
  puts "About to start getting data for companies beginning with #{letters}"
  i = 1
  next_page_link = true
  while next_page_link do
    json_data = '{"Start":"' + i.to_s + '","Name":"' + letters.to_s + 
   '","Criteria":"all","NameType":"starts_with","UBI":"","Active":"","AgentName":"","City":"","Zip":"","Domestic":"","Category":"","Now":' +
      (Time.now.to_f*1000).to_i.to_s + ',"StartDate":"","EndDate":""}'
    data = @http.post(@path, json_data, @headers).read_body 
    page = Nokogiri::HTML(JSON.parse(data)['d'])
    scrape_page(page)
    i += 20
    next_page_link = page.at('a[@href*="javascript:showNext"]')
  end
rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
  puts "Exception raised while getting data: #{e.inspect}\nParams:#{json_data.inspect}"
end

# This is where the script proper starts

@http = Net::HTTP.new("www.sos.wa.gov")
@path = "/corps/search_detail201002.asmx/GetNext"
@headers = { 'Accept' => '*/*', 'Content-Type' => 'application/json; charset=utf-8' }

start_position = POSSIBLE_PREFIXES.index ScraperWiki.get_var('letters', "AA")

POSSIBLE_PREFIXES[start_position..-1].each do |letters|
  ScraperWiki.save_var('letters', letters) # save letters in case scraper gets killed
  get_results_and_extract_data_for(letters)
  puts "\nFinished getting details for companies beginning with '#{letters}'\n"
end

ScraperWiki.save_var('letters', 'AA') # if we've got this far it's because we've done all letters
