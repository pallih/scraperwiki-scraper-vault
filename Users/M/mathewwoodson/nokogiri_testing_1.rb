# Blank Ruby
# example code from http://nokogiri.org/

require 'nokogiri'
require 'open-uri'
require 'scraperwiki'
require 'csv'

input = ScraperWiki::scrape("http://www.virginisles.com/subs1.csv") 

csv = CSV.new(input)
puts "Got the CSV"

for row in csv
  test = row[0]
  begin  
    # Get a Nokogiri::HTML:Document for the page weâ€™re interested in...
    target = 'http://www.google.com/search?q=site%3A' + test
    doc = Nokogiri::HTML(open(target))
    #puts "Got the doc"
  rescue Exception => e
    target = e.message
  end
  puts target
  #puts doc.inspect

  # Do funky things with it using Nokogiri::XML::Node methods...
  ####
  # Search for nodes by css
  
  found = doc.at_css('#subform_ctrl')
  if found   
    split = found.text.split
    num = split[2]
  else
    num = "0"
  end
  ScraperWiki::save_sqlite(unique_keys=["domain"], data={ "domain" => test, "results" => num })
  puts "Saved #{test}: #{num}"
  

  if rand() < 0.1
    r = 53.11 + rand*3.76
  else
    r = rand*3.94 + 11.532
  end
  puts "sleeping #{r.to_s}"
  sleep(r)

end


=begin
    doc.css('h3.r a').each do |link|
      begin
        raw = link['href']
        #puts raw    
        start = raw.index("?q=")+3
        tail = raw.index("&sa=")
        #puts "#{start.to_s} and #{tail.to_s}"
        url = raw.slice(start, tail-start)

        #puts key
      rescue Exception => e
        url = e.message    
      end
        i += 1
        puts "#{i.to_s}: #{url}"
        key = "#{new}-#{i.to_s}"
        ScraperWiki::save_sqlite(unique_keys=["a"], data={ "a" => key, "kw" => test, "rank" => i, "url" => url })
      #puts "stored"
    end
=end


# Blank Ruby
# example code from http://nokogiri.org/

require 'nokogiri'
require 'open-uri'
require 'scraperwiki'
require 'csv'

input = ScraperWiki::scrape("http://www.virginisles.com/subs1.csv") 

csv = CSV.new(input)
puts "Got the CSV"

for row in csv
  test = row[0]
  begin  
    # Get a Nokogiri::HTML:Document for the page weâ€™re interested in...
    target = 'http://www.google.com/search?q=site%3A' + test
    doc = Nokogiri::HTML(open(target))
    #puts "Got the doc"
  rescue Exception => e
    target = e.message
  end
  puts target
  #puts doc.inspect

  # Do funky things with it using Nokogiri::XML::Node methods...
  ####
  # Search for nodes by css
  
  found = doc.at_css('#subform_ctrl')
  if found   
    split = found.text.split
    num = split[2]
  else
    num = "0"
  end
  ScraperWiki::save_sqlite(unique_keys=["domain"], data={ "domain" => test, "results" => num })
  puts "Saved #{test}: #{num}"
  

  if rand() < 0.1
    r = 53.11 + rand*3.76
  else
    r = rand*3.94 + 11.532
  end
  puts "sleeping #{r.to_s}"
  sleep(r)

end


=begin
    doc.css('h3.r a').each do |link|
      begin
        raw = link['href']
        #puts raw    
        start = raw.index("?q=")+3
        tail = raw.index("&sa=")
        #puts "#{start.to_s} and #{tail.to_s}"
        url = raw.slice(start, tail-start)

        #puts key
      rescue Exception => e
        url = e.message    
      end
        i += 1
        puts "#{i.to_s}: #{url}"
        key = "#{new}-#{i.to_s}"
        ScraperWiki::save_sqlite(unique_keys=["a"], data={ "a" => key, "kw" => test, "rank" => i, "url" => url })
      #puts "stored"
    end
=end


