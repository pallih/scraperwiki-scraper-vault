# Ruby scraper for walesoffice.gov.uk speeches
require 'nokogiri'
require 'uri'

def alternate_name(name)
  alternates = { 'chris' => 'christopher', 'greg' => 'gregory', 'nick' => 'nicholas' }
  # And add the inverse alternatives
  alternates.each { |k, v| alternates[v] = k }
  # Return the alternative if it's available
  alternates[name.downcase]
end
  
# Function to search a list of members of parliament from parlparse, given the URL for the parlparse list
def find_member_from_url(name, url)
  #puts "Looking for #{name} in #{url}"
  # Retrieve a list of members of parliament from parlparse
  member_html = ScraperWiki.scrape(url)
  member_doc = Nokogiri::HTML(member_html)
  # Build a list of names for easy comparison
  members = {}
  member_doc.css('member').each do |m| 
    members[m['firstname'].downcase+" "+m['lastname'].downcase] = m
    # See if there's an alternative name option (e.g. Christopher and Chris are synonyms)
    if alternate_name(m['firstname'])
      # Just add this as an extra value in the hash
      members[alternate_name(m['firstname']).downcase+" "+m['lastname'].downcase] = m
    end
  end
  members[name.downcase]
end
  
# Function to search a list of lords from parlparse, given the URL for the parlparse list
def find_lord_from_url(name, url)
  #puts "Looking for lord #{name} in #{url}"
  # Retrieve a list of lords from parlparse
  lords_html = ScraperWiki.scrape(url)
  lords_doc = Nokogiri::HTML(lords_html)
  # Build a list of names for easy comparison
  lords = {}
  lords_doc.css('lord').each do |l| 
    lords[l['title'].downcase+" "+l['lordname'].downcase] = l
    unless l['forenames'].nil? 
      lords[l['title'].downcase+" "+l['forenames'].downcase+" "+l['lordname'].downcase] = l
    end
  end
  lords[name.downcase]
end
  
# Function to map a given name to a parlparse member
# Returns either an MP or a Lord - these have different attributes, unfortunately, but both have an 'id'
def find_member(name)
  # Do some crude preprocessing of "name"
  name = name.downcase
  # Check for extra clauses with a ','
  if name.index(',')
    clauses = name.split(',')
    # Use the clause that doesn't contain the word "minister"
    if clauses[0].match(/minister/)
      name = clauses[1]
    else
      name = clauses[0]
    end
  end
  # Now remove any remaining titles that we don't care about
  name.gsub!("rt hon", "")
  name.gsub!("deputy prime minister", "")
  name.gsub!("prime minister", "")
  name.gsub!("foreign secretary", "")
  name.gsub!("foreign office minister", "")
  name.gsub!("minister for europe", "")
  name.gsub!("minister", "") # Note this needs to be *after* any others including the word "minister"
  name.gsub!("mr ", "")
  name.gsub!(" mp", "")
  name.gsub!("sir ", "")
  name.strip!
 
  member = find_member_from_url(name, 'http://ukparse.kforge.net/svn/parlparse/members/all-members.xml')
  if member.nil? 
    member = find_member_from_url(name, 'http://ukparse.kforge.net/svn/parlparse/members/all-members-2010.xml')
    if member.nil? 
      member = find_lord_from_url(name, 'http://ukparse.kforge.net/svn/parlparse/members/peers-ucl.xml')
    end
  end
  member
end
 
def get_member_name(member)
  if member.nil? 
    ""
  elsif member['firstname']
    # It's a member
    member['firstname']+' '+member['lastname']
  else
    # It's a lord
    member['title']+' '+member['lordname']
  end
end

# retrieve the news index page
base_url = "http://www.walesoffice.gov.uk/category/speeches/"
starting_url = base_url

puts "Getting "+starting_url
parsed_base_url = URI.parse(starting_url)
html = ScraperWiki.scrape(starting_url)
 
doc = Nokogiri::HTML(html)
 
# And now scrape the speeches
doc.css('#main p b a').each do |speech|
  record = {'permalink' => parsed_base_url.merge(speech['href']).to_s,
            'department' => 'Wales Office'}
  puts "Looking at #{speech.inner_text}"
  puts "=> "+record['permalink']
  the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
  the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

  record['title'] = the_speech_doc.css('h2.pagetitle')[0].inner_text
  record['given_on'] = Date.parse(the_speech_doc.css('div.meta').inner_text).to_s
  # The date and location are usually in the first two paragraphs at the start of the speech
  # if the first paragraph is <strong> and not the text "Introduction"
  initial_paras = the_speech_doc.css('#main p')[0..1]
  if !initial_paras[0].css('strong').empty? && initial_paras[0].inner_text.downcase != "introduction"
    begin
      # See if there's a date in the second paragraph
      Date.parse(initial_paras[1].inner_text)
      # if so then the location is in the first paragraph
      record['where'] = initial_paras[0].inner_text
    rescue
      # Date isn't in the second paragraph, so it'll be the location
      record['where'] = initial_paras[1].inner_text
    end
  end

  # If the parlparse ministers.xml was more up-to-date, then we could possibly do something more intelligent here
  # For now, just assume it was given by the current Secretary of State for Wales
  member = find_member("Cheryl Gillan")
  if member.nil? 
    raise "#### ERROR: Couldn't find member details for #{full}"
  else
    record['minister_name'] = get_member_name(member)
    record['minister_parlparse_id'] = member['id']
  end

  record['body'] = the_speech_doc.css('#main p').collect { |para| para.to_s }.join("\n\n") 
  begin
    ScraperWiki.save(['permalink'], record)
  rescue => e
    puts e.message
    puts record.inspect
  end
end

# At present all of the speeches fit onto one page so it isn't clear if there'll be pagination or not
# As a simple check that things haven't overflowed onto a second page, see if there's still a link to
# the earliest speech available now
unless doc.css('#main p b a').last['href'] == 'http://www.walesoffice.gov.uk/2010/06/16/cheryl-gillans-address-to-the-national-assembly-for-wales-on-the-queen%e2%80%99s-speech/'
  raise "#### ERROR: Last speech link has changed. Does the speeches page now paginate?"
end

