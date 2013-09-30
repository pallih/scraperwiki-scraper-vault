# Blank Ruby
# example code from http://nokogiri.org/

require 'nokogiri'
require 'open-uri'
require 'scraperwiki'

playground = ["usury law","cat hunting","chicago car accident lawyer","interpretation equipment","driving under the influence of marijuana"]
playground.each do |test|
  
  new = test.gsub(" ","+")
  puts test  
  begin  
    # Get a Nokogiri::HTML:Document for the page weâ€™re interested in...
    target = 'http://www.google.com/search?q=' + new + '&pws=0&num=25'
    doc = Nokogiri::HTML(open(target))
    puts "Got the doc"
  rescue Exception => e
    target = e.message
  end
  puts target

  # Do funky things with it using Nokogiri::XML::Node methods...
  ####
  # Search for nodes by css
  i = 200
  
    biggie = doc.css('h3.r a')
    puts biggie.inspect
    biggie.each do |link|
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
  if rand() < 0.0
    r = 53.11 + rand*3.76
  else
    r = rand*2 + 2.3
  end
  puts "sleeping #{r.to_s}"
  sleep(r)
end

=begin
def clean(raw)
  url = ""  
  if raw.match(/\/url\?q=/)
    url = get_inside(self, "?q=", "&amp")
  end
  return (url != '') ?  url : "error"
end

def get_inside(haystack, start, tail)
  start_index = haystack.index(start)+start.length
  end_index = haystack.index(tail)
  return haystack.slice(start_index, end_index - start_index)
end
=end

=begin
####
# Search for nodes by xpath
doc.xpath('//h3/a[@class="l"]').each do |link|
    puts link.content
end

####
# Or mix and match.
doc.search('h3.r a.l', '//h3/a[@class="l"]').each do |link|
    puts link.content
end
=end
# Blank Ruby
# example code from http://nokogiri.org/

require 'nokogiri'
require 'open-uri'
require 'scraperwiki'

playground = ["usury law","cat hunting","chicago car accident lawyer","interpretation equipment","driving under the influence of marijuana"]
playground.each do |test|
  
  new = test.gsub(" ","+")
  puts test  
  begin  
    # Get a Nokogiri::HTML:Document for the page weâ€™re interested in...
    target = 'http://www.google.com/search?q=' + new + '&pws=0&num=25'
    doc = Nokogiri::HTML(open(target))
    puts "Got the doc"
  rescue Exception => e
    target = e.message
  end
  puts target

  # Do funky things with it using Nokogiri::XML::Node methods...
  ####
  # Search for nodes by css
  i = 200
  
    biggie = doc.css('h3.r a')
    puts biggie.inspect
    biggie.each do |link|
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
  if rand() < 0.0
    r = 53.11 + rand*3.76
  else
    r = rand*2 + 2.3
  end
  puts "sleeping #{r.to_s}"
  sleep(r)
end

=begin
def clean(raw)
  url = ""  
  if raw.match(/\/url\?q=/)
    url = get_inside(self, "?q=", "&amp")
  end
  return (url != '') ?  url : "error"
end

def get_inside(haystack, start, tail)
  start_index = haystack.index(start)+start.length
  end_index = haystack.index(tail)
  return haystack.slice(start_index, end_index - start_index)
end
=end

=begin
####
# Search for nodes by xpath
doc.xpath('//h3/a[@class="l"]').each do |link|
    puts link.content
end

####
# Or mix and match.
doc.search('h3.r a.l', '//h3/a[@class="l"]').each do |link|
    puts link.content
end
=end
