require 'rubygems'
require 'mechanize'

agent = Mechanize.new
url = 'http://www.vcat.vic.gov.au/CA256DBB0022825D/page/Daily+Law+List-Residential+Tenancies+List?OpenDocument&1=20-Daily+Law+List~&2=20-Residential+Tenancies+List~&3=~'

page = agent.get(url)

page.at("div.DOCbody").search("tr").each do |r|
  if r.children.count == 1
    @date = Date.parse(r.inner_text) if r.inner_text != ""
    next
  elsif r.children.count == 2
    @venue = r.children[1].inner_text if r.children[0].inner_text == 'Town:'
    @location = r.children[1].inner_text if r.children[0].inner_text == 'Venue:'
    next
  elsif r.children.count == 3
    next if r.children[0].inner_text.strip == "Time"
  end
  
  hearing = {
    'unique_id'           => @date.to_s + r.children[2].inner_text,
    'case_number'         => r.children[2].inner_text,
    'party_a'             => r.children[1].inner_text.split(" vs ")[0],
    'party_b'             => r.children[1].inner_text.split(" vs ")[1],
    'date'                => @date,
    'time'                => r.children[0].inner_text[0..-5],
    'location'            => @location,
    'venue'               => @venue,
    'venue_postcode'      => @location[-4..-1]
  }
  
  ScraperWiki.save(['unique_id'], hearing)
end
require 'rubygems'
require 'mechanize'

agent = Mechanize.new
url = 'http://www.vcat.vic.gov.au/CA256DBB0022825D/page/Daily+Law+List-Residential+Tenancies+List?OpenDocument&1=20-Daily+Law+List~&2=20-Residential+Tenancies+List~&3=~'

page = agent.get(url)

page.at("div.DOCbody").search("tr").each do |r|
  if r.children.count == 1
    @date = Date.parse(r.inner_text) if r.inner_text != ""
    next
  elsif r.children.count == 2
    @venue = r.children[1].inner_text if r.children[0].inner_text == 'Town:'
    @location = r.children[1].inner_text if r.children[0].inner_text == 'Venue:'
    next
  elsif r.children.count == 3
    next if r.children[0].inner_text.strip == "Time"
  end
  
  hearing = {
    'unique_id'           => @date.to_s + r.children[2].inner_text,
    'case_number'         => r.children[2].inner_text,
    'party_a'             => r.children[1].inner_text.split(" vs ")[0],
    'party_b'             => r.children[1].inner_text.split(" vs ")[1],
    'date'                => @date,
    'time'                => r.children[0].inner_text[0..-5],
    'location'            => @location,
    'venue'               => @venue,
    'venue_postcode'      => @location[-4..-1]
  }
  
  ScraperWiki.save(['unique_id'], hearing)
end
require 'rubygems'
require 'mechanize'

agent = Mechanize.new
url = 'http://www.vcat.vic.gov.au/CA256DBB0022825D/page/Daily+Law+List-Residential+Tenancies+List?OpenDocument&1=20-Daily+Law+List~&2=20-Residential+Tenancies+List~&3=~'

page = agent.get(url)

page.at("div.DOCbody").search("tr").each do |r|
  if r.children.count == 1
    @date = Date.parse(r.inner_text) if r.inner_text != ""
    next
  elsif r.children.count == 2
    @venue = r.children[1].inner_text if r.children[0].inner_text == 'Town:'
    @location = r.children[1].inner_text if r.children[0].inner_text == 'Venue:'
    next
  elsif r.children.count == 3
    next if r.children[0].inner_text.strip == "Time"
  end
  
  hearing = {
    'unique_id'           => @date.to_s + r.children[2].inner_text,
    'case_number'         => r.children[2].inner_text,
    'party_a'             => r.children[1].inner_text.split(" vs ")[0],
    'party_b'             => r.children[1].inner_text.split(" vs ")[1],
    'date'                => @date,
    'time'                => r.children[0].inner_text[0..-5],
    'location'            => @location,
    'venue'               => @venue,
    'venue_postcode'      => @location[-4..-1]
  }
  
  ScraperWiki.save(['unique_id'], hearing)
end
