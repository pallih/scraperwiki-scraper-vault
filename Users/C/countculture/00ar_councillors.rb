# Blank Ruby
#import scraperwiki
#import BeautifulSoup
#import re

#from scraperwiki import datastore

# Getting names and URLs of London Borough of Havering councillors #

#scrape page
#html = scraperwiki.scrape('http://www.havering.gov.uk/index.aspx?articleid=627')
#page = BeautifulSoup.BeautifulSoup(html)

#get list of wards
#for ward_link in page.find(id='lhscol').findAll('a', title=re.compile("Ward")):
#    ward_page = BeautifulSoup.BeautifulSoup(scraperwiki.scrape(ward_link['href']))
    #get councillors for each ward
#    for councillor_link in ward_page.find(id='lhscol').findAll('a', title=re.compile("Councillor ")):
#        url = councillor_link['href']
#        full_name = councillor_link.string
#        uid = re.search(r'id=(\d+)', url).group(1)
        #print full_name, url, uid
        
        #save to datastore
#        data = {'full_name' : full_name, 'url' : url, 'uid' : uid,}
#        datastore.save(unique_keys=['uid'], data=data)

require 'rubygems'
require 'nokogiri'
#require 'net/http'
#require 'json'

# ScraperWiki.sqliteexecute("DELETE from swdata where CompanyNumber = ''")
# exit

# scrape_page function: gets passed an individual page to scrape
# def scrape_page(page)
#  page.css('ul.CorpsListItems li a').collect do |link|
#    record = {'CompanyName'  => link.content.strip,
#              'CompanyNumber'=> link[:onclick].scan(/\d+/).to_s,
#              'date_scraped' => Time.now
             }
#    next if record['CompanyNumber'].nil? || record['CompanyNumber'] == '' 
#    ScraperWiki.save(["CompanyNumber"], record)
#  end
#rescue Exception => e
#  puts "Exception raised while getting or parsing data: #{e.inspect}"
#end
        
#def get_results_and_extract_data_for(letter)
#  puts "About to start getting data for companies beginning with #{letter}"
#  i = 1
#  next_page_link = true
#  while next_page_link do
#    json_data = '{"Start":"' + i.to_s + '","Name":"' + letter.to_s + 
#  '","Criteria":"all","NameType":"starts_with","UBI":"","Active":"","AgentName":"","City":"","Zip":"","Domestic":"","Category":"","Now":' +
#      (Time.now.to_f*1000).to_i.to_s + ',"StartDate":"","EndDate":""}'
#    data = @http.post(@path, json_data, @headers).read_body 
#    page = Nokogiri::HTML(JSON.parse(data)['d'])
#    scrape_page(page)
#    i += 20
#    next_page_link = page.at('a[@href*="javascript:showNext"]')
#  end
#rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, #don't worry about missing a few entries
#  puts "Exception raised while getting data: #{e.inspect}\nParams:#{json_data.inspect}"
end

# This is where the script proper starts

@http = Net::HTTP.new("www.sos.wa.gov")
@path = "/corps/search_detail201002.asmx/GetNext"
@headers = { 'Accept' => '*/*', 'Content-Type' => 'application/json; charset=utf-8' }

initial_chars = (0..9).to_a + ('A'..'Z').to_a
start_position = initial_chars.index ScraperWiki.get_var('letter', 0)

initial_chars[start_position..-1].each do |letter|
  ScraperWiki.save_var('letter', letter) # save letter in case scraper gets killed
  get_results_and_extract_data_for(letter)
  puts "\nFinished getting details for companies beginning with '#{letter}'\n"
end

ScraperWiki.save_var('letter', 0) # if we've got this far it's because we've done all letters# Blank Ruby
#import scraperwiki
#import BeautifulSoup
#import re

#from scraperwiki import datastore

# Getting names and URLs of London Borough of Havering councillors #

#scrape page
#html = scraperwiki.scrape('http://www.havering.gov.uk/index.aspx?articleid=627')
#page = BeautifulSoup.BeautifulSoup(html)

#get list of wards
#for ward_link in page.find(id='lhscol').findAll('a', title=re.compile("Ward")):
#    ward_page = BeautifulSoup.BeautifulSoup(scraperwiki.scrape(ward_link['href']))
    #get councillors for each ward
#    for councillor_link in ward_page.find(id='lhscol').findAll('a', title=re.compile("Councillor ")):
#        url = councillor_link['href']
#        full_name = councillor_link.string
#        uid = re.search(r'id=(\d+)', url).group(1)
        #print full_name, url, uid
        
        #save to datastore
#        data = {'full_name' : full_name, 'url' : url, 'uid' : uid,}
#        datastore.save(unique_keys=['uid'], data=data)

require 'rubygems'
require 'nokogiri'
#require 'net/http'
#require 'json'

# ScraperWiki.sqliteexecute("DELETE from swdata where CompanyNumber = ''")
# exit

# scrape_page function: gets passed an individual page to scrape
# def scrape_page(page)
#  page.css('ul.CorpsListItems li a').collect do |link|
#    record = {'CompanyName'  => link.content.strip,
#              'CompanyNumber'=> link[:onclick].scan(/\d+/).to_s,
#              'date_scraped' => Time.now
             }
#    next if record['CompanyNumber'].nil? || record['CompanyNumber'] == '' 
#    ScraperWiki.save(["CompanyNumber"], record)
#  end
#rescue Exception => e
#  puts "Exception raised while getting or parsing data: #{e.inspect}"
#end
        
#def get_results_and_extract_data_for(letter)
#  puts "About to start getting data for companies beginning with #{letter}"
#  i = 1
#  next_page_link = true
#  while next_page_link do
#    json_data = '{"Start":"' + i.to_s + '","Name":"' + letter.to_s + 
#  '","Criteria":"all","NameType":"starts_with","UBI":"","Active":"","AgentName":"","City":"","Zip":"","Domestic":"","Category":"","Now":' +
#      (Time.now.to_f*1000).to_i.to_s + ',"StartDate":"","EndDate":""}'
#    data = @http.post(@path, json_data, @headers).read_body 
#    page = Nokogiri::HTML(JSON.parse(data)['d'])
#    scrape_page(page)
#    i += 20
#    next_page_link = page.at('a[@href*="javascript:showNext"]')
#  end
#rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, #don't worry about missing a few entries
#  puts "Exception raised while getting data: #{e.inspect}\nParams:#{json_data.inspect}"
end

# This is where the script proper starts

@http = Net::HTTP.new("www.sos.wa.gov")
@path = "/corps/search_detail201002.asmx/GetNext"
@headers = { 'Accept' => '*/*', 'Content-Type' => 'application/json; charset=utf-8' }

initial_chars = (0..9).to_a + ('A'..'Z').to_a
start_position = initial_chars.index ScraperWiki.get_var('letter', 0)

initial_chars[start_position..-1].each do |letter|
  ScraperWiki.save_var('letter', letter) # save letter in case scraper gets killed
  get_results_and_extract_data_for(letter)
  puts "\nFinished getting details for companies beginning with '#{letter}'\n"
end

ScraperWiki.save_var('letter', 0) # if we've got this far it's because we've done all letters