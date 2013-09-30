require 'rubygems'
require 'nokogiri'
require 'mechanize'

agent = Mechanize.new

url = "http://eservices.portstephens.nsw.gov.au/eservice/daEnquiry/currentlyAdvertised.do?nodeNum=35701"

doc = agent.get(url)


items = doc.at("div#fullcontent").search("div")[6]

items.search("div").each do |i|
  #reference number
  i.search("span.key").each do |s|
    case s.inner_text
    when "Application No."
      @council_reference = s.next.inner_text
    when "Date Lodged"
      @date_received = s.next.inner_text
    end
  end

  #address
 
  addr = i.previous.at("a.plain_header")

  next if addr.nil? 
  @address = addr.inner_text
  @info_url = 'http://eservices.portstephens.nsw.gov.au' + addr['href'].strip
    
  sleep(1)
  
  da_info = agent.get(@info_url) #get description page
    
  da_items = da_info.at("div#fullcontent").search("div")[5]
  da_items.search("span.key").each do |dai|
    if dai.inner_text == "Type of Work"
       @description = dai.next.inner_text
    end
  end

  record = {
    'info_url' => url,
    'comment_url' => "mailto:Council@portstephens.nsw.gov.au",
    'council_reference' => @council_reference,
    'date_received' => Date.strptime(@date_received.strip, '%d/%m/%Y').to_s,
    'address' => @address,
    'description' => @description,
    'date_scraped' => Date.today.to_s
  }  


  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
   ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end

end
require 'rubygems'
require 'nokogiri'
require 'mechanize'

agent = Mechanize.new

url = "http://eservices.portstephens.nsw.gov.au/eservice/daEnquiry/currentlyAdvertised.do?nodeNum=35701"

doc = agent.get(url)


items = doc.at("div#fullcontent").search("div")[6]

items.search("div").each do |i|
  #reference number
  i.search("span.key").each do |s|
    case s.inner_text
    when "Application No."
      @council_reference = s.next.inner_text
    when "Date Lodged"
      @date_received = s.next.inner_text
    end
  end

  #address
 
  addr = i.previous.at("a.plain_header")

  next if addr.nil? 
  @address = addr.inner_text
  @info_url = 'http://eservices.portstephens.nsw.gov.au' + addr['href'].strip
    
  sleep(1)
  
  da_info = agent.get(@info_url) #get description page
    
  da_items = da_info.at("div#fullcontent").search("div")[5]
  da_items.search("span.key").each do |dai|
    if dai.inner_text == "Type of Work"
       @description = dai.next.inner_text
    end
  end

  record = {
    'info_url' => url,
    'comment_url' => "mailto:Council@portstephens.nsw.gov.au",
    'council_reference' => @council_reference,
    'date_received' => Date.strptime(@date_received.strip, '%d/%m/%Y').to_s,
    'address' => @address,
    'description' => @description,
    'date_scraped' => Date.today.to_s
  }  


  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
   ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end

end
