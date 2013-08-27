require 'open-uri'
require 'nokogiri'
require 'benchmark'

def save_company(abn)
  api_result = Nokogiri.parse(open("http://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/ABRSearchByABN?searchString=#{abn}&includeHistoricalDetails=Y&authenticationGuid=082f1497-93ff-4fc3-9c85-030022b11840"))

  main_record = {"ABN" => abn}

  api_result.at('businessentity').children.each do |detail|
    if detail.children.size == 1
      # Record single bits of detail in the main DB as it's key is unique
      main_record[detail.name] = detail.text
    elsif detail.children.size > 1
      # Record larger bits of detail in its own DB as it's often not unique, i.e. historical detail
      record = {"ABN" => abn}
      detail.children.each { |r| record[r.name] = r.text }
      ScraperWiki.save_sqlite ["ABN"], record , detail.name
    else
      # Ignore blank records
    end
  end

  ScraperWiki.save_sqlite ["ABN"], main_record
end

ScraperWiki.attach('australian_business_numbers')
offset = ScraperWiki.get_var('offset')
if offset == nil 
  offset = 0
end

while true do
  abns = ScraperWiki.select("abn from australian_business_numbers.swdata limit 10 offset #{offset}")
  break if abns.empty? 

  abns.each do |item|
    next unless ScraperWiki.select("* from swdata where ABN=#{item['abn']}").empty? 

    puts "Getting ABN #{item['abn']}"
    time = Benchmark.realtime do
      save_company(item['abn'])
    end 
    puts "Parsed and saved in #{(time*1000).ceil} ms"
  end
  offset += 10
  ScraperWiki.save_var('offset', offset)
end


offset = 0
ScraperWiki.save_var('offset', offset)
require 'open-uri'
require 'nokogiri'
require 'benchmark'

def save_company(abn)
  api_result = Nokogiri.parse(open("http://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/ABRSearchByABN?searchString=#{abn}&includeHistoricalDetails=Y&authenticationGuid=082f1497-93ff-4fc3-9c85-030022b11840"))

  main_record = {"ABN" => abn}

  api_result.at('businessentity').children.each do |detail|
    if detail.children.size == 1
      # Record single bits of detail in the main DB as it's key is unique
      main_record[detail.name] = detail.text
    elsif detail.children.size > 1
      # Record larger bits of detail in its own DB as it's often not unique, i.e. historical detail
      record = {"ABN" => abn}
      detail.children.each { |r| record[r.name] = r.text }
      ScraperWiki.save_sqlite ["ABN"], record , detail.name
    else
      # Ignore blank records
    end
  end

  ScraperWiki.save_sqlite ["ABN"], main_record
end

ScraperWiki.attach('australian_business_numbers')
offset = ScraperWiki.get_var('offset')
if offset == nil 
  offset = 0
end

while true do
  abns = ScraperWiki.select("abn from australian_business_numbers.swdata limit 10 offset #{offset}")
  break if abns.empty? 

  abns.each do |item|
    next unless ScraperWiki.select("* from swdata where ABN=#{item['abn']}").empty? 

    puts "Getting ABN #{item['abn']}"
    time = Benchmark.realtime do
      save_company(item['abn'])
    end 
    puts "Parsed and saved in #{(time*1000).ceil} ms"
  end
  offset += 10
  ScraperWiki.save_var('offset', offset)
end


offset = 0
ScraperWiki.save_var('offset', offset)
require 'open-uri'
require 'nokogiri'
require 'benchmark'

def save_company(abn)
  api_result = Nokogiri.parse(open("http://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/ABRSearchByABN?searchString=#{abn}&includeHistoricalDetails=Y&authenticationGuid=082f1497-93ff-4fc3-9c85-030022b11840"))

  main_record = {"ABN" => abn}

  api_result.at('businessentity').children.each do |detail|
    if detail.children.size == 1
      # Record single bits of detail in the main DB as it's key is unique
      main_record[detail.name] = detail.text
    elsif detail.children.size > 1
      # Record larger bits of detail in its own DB as it's often not unique, i.e. historical detail
      record = {"ABN" => abn}
      detail.children.each { |r| record[r.name] = r.text }
      ScraperWiki.save_sqlite ["ABN"], record , detail.name
    else
      # Ignore blank records
    end
  end

  ScraperWiki.save_sqlite ["ABN"], main_record
end

ScraperWiki.attach('australian_business_numbers')
offset = ScraperWiki.get_var('offset')
if offset == nil 
  offset = 0
end

while true do
  abns = ScraperWiki.select("abn from australian_business_numbers.swdata limit 10 offset #{offset}")
  break if abns.empty? 

  abns.each do |item|
    next unless ScraperWiki.select("* from swdata where ABN=#{item['abn']}").empty? 

    puts "Getting ABN #{item['abn']}"
    time = Benchmark.realtime do
      save_company(item['abn'])
    end 
    puts "Parsed and saved in #{(time*1000).ceil} ms"
  end
  offset += 10
  ScraperWiki.save_var('offset', offset)
end


offset = 0
ScraperWiki.save_var('offset', offset)
