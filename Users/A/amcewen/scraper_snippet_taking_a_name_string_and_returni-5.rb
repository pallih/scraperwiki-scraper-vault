# NOTE: The version in the FCO scraper is a better implementation of this, and should be moved into here sometime or other...

# Not a full scraper, but a snippet to get the MP details from parlparse when given an MP's name (or a Lord's name)
# Generally going to be cut-and-pasted into another scraper when you're retrieving names of people in parliament and
# you want to store a parlparse ID along with their name
# Hopefully copes with names like "Chris Huhne" when parlparse gives him as "Christopher Huhne"
require 'nokogiri'
require 'uri'
  
def alternate_name(name)
  alternates = { 'chris' => 'christopher', 'greg' => 'gregory', 'nick' => 'nicholas', 'ed' => 'edward' }
  # And add the inverse alternatives
  alternates.each { |k, v| alternates[v] = k }
  # Return the alternative if it's available
  alternates[name.downcase]
end
  
# Function to search a list of members of parliament from parlparse, given the URL for the parlparse list
def find_member_from_url(name, url)
  puts "Looking for #{name} in #{url}"
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
  puts "Looking for lord #{name} in #{url}"
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
  if name.nil? 
    return nil
  end
  # Do some crude preprocessing of "name"
  name = name.downcase
  # Check for extra clauses with a ','
  if name.index(',')
    clauses = name.split(',')
    # Use the clause that doesn't contain the word "minister"
    if clauses[0].match(/minister|secretary/)
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
  name.gsub!("international development minister", "")
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

#### This function is only needed if you don't get member names, but get ministerial positions instead
def get_minister_name(dept, position, minister_date)
  dept_shortnames = { "Ministry of Defence" => "Defence" }
  # Retrieve a list of members of parliament from parlparse
  minister_html = ScraperWiki.scrape('http://ukparse.kforge.net/svn/parlparse/members/ministers.xml')
  minister_doc = Nokogiri::HTML(minister_html)
  # See if we can find the given position
  minister_name = nil
  ministers = minister_doc.css("moffice[dept='#{dept}'][position='#{position}']")
  if ministers.empty? 
    # We didn't get any matches, it could be because we're looking for "Secretary of State" for example,
    # when in the parlparse data that would be "Secretary of State for Defence", so try adding that
    position = position+" for "+dept_shortnames[dept]
    ministers = minister_doc.css("moffice[dept='#{dept}'][position='#{position}']")
  end
  ministers.each do |m|
puts m.inspect
    begin
      start_date = Date.parse(m['fromdate'])
puts "start "+start_date.to_s
      end_date = Date.parse(m['todate'])
puts "end "+end_date.to_s
      search_date = Date.strptime(minister_date, "%d/%M/%Y")
      if search_date >= start_date && search_date < end_date
        # We've found who we want
        minister_name = m['name']
      end
    rescue
puts "exception"
    end
  end
  minister_name
end
#### 

#puts get_minister_name("Ministry of Defence", "Secretary of State", "22/02/2011")

henry = find_member("UK Minister for Africa, Mr Henry Bellingham MP")
puts "Henry resolved to "+get_member_name(henry)+", details: "+henry.inspect
 
#chris = find_member("Chris Huhne")
#puts "Chris resolved to "+get_member_name(chris)+", details: "+chris.inspect
#fred = find_member("fred dibner")
#puts "Fred: "+get_member_name(fred)+", details: "+fred.inspect
#lord = find_member("Lord Marland")
#puts "Lord: "+get_member_name(lord)+", details: "+lord.inspect
 # NOTE: The version in the FCO scraper is a better implementation of this, and should be moved into here sometime or other...

# Not a full scraper, but a snippet to get the MP details from parlparse when given an MP's name (or a Lord's name)
# Generally going to be cut-and-pasted into another scraper when you're retrieving names of people in parliament and
# you want to store a parlparse ID along with their name
# Hopefully copes with names like "Chris Huhne" when parlparse gives him as "Christopher Huhne"
require 'nokogiri'
require 'uri'
  
def alternate_name(name)
  alternates = { 'chris' => 'christopher', 'greg' => 'gregory', 'nick' => 'nicholas', 'ed' => 'edward' }
  # And add the inverse alternatives
  alternates.each { |k, v| alternates[v] = k }
  # Return the alternative if it's available
  alternates[name.downcase]
end
  
# Function to search a list of members of parliament from parlparse, given the URL for the parlparse list
def find_member_from_url(name, url)
  puts "Looking for #{name} in #{url}"
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
  puts "Looking for lord #{name} in #{url}"
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
  if name.nil? 
    return nil
  end
  # Do some crude preprocessing of "name"
  name = name.downcase
  # Check for extra clauses with a ','
  if name.index(',')
    clauses = name.split(',')
    # Use the clause that doesn't contain the word "minister"
    if clauses[0].match(/minister|secretary/)
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
  name.gsub!("international development minister", "")
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

#### This function is only needed if you don't get member names, but get ministerial positions instead
def get_minister_name(dept, position, minister_date)
  dept_shortnames = { "Ministry of Defence" => "Defence" }
  # Retrieve a list of members of parliament from parlparse
  minister_html = ScraperWiki.scrape('http://ukparse.kforge.net/svn/parlparse/members/ministers.xml')
  minister_doc = Nokogiri::HTML(minister_html)
  # See if we can find the given position
  minister_name = nil
  ministers = minister_doc.css("moffice[dept='#{dept}'][position='#{position}']")
  if ministers.empty? 
    # We didn't get any matches, it could be because we're looking for "Secretary of State" for example,
    # when in the parlparse data that would be "Secretary of State for Defence", so try adding that
    position = position+" for "+dept_shortnames[dept]
    ministers = minister_doc.css("moffice[dept='#{dept}'][position='#{position}']")
  end
  ministers.each do |m|
puts m.inspect
    begin
      start_date = Date.parse(m['fromdate'])
puts "start "+start_date.to_s
      end_date = Date.parse(m['todate'])
puts "end "+end_date.to_s
      search_date = Date.strptime(minister_date, "%d/%M/%Y")
      if search_date >= start_date && search_date < end_date
        # We've found who we want
        minister_name = m['name']
      end
    rescue
puts "exception"
    end
  end
  minister_name
end
#### 

#puts get_minister_name("Ministry of Defence", "Secretary of State", "22/02/2011")

henry = find_member("UK Minister for Africa, Mr Henry Bellingham MP")
puts "Henry resolved to "+get_member_name(henry)+", details: "+henry.inspect
 
#chris = find_member("Chris Huhne")
#puts "Chris resolved to "+get_member_name(chris)+", details: "+chris.inspect
#fred = find_member("fred dibner")
#puts "Fred: "+get_member_name(fred)+", details: "+fred.inspect
#lord = find_member("Lord Marland")
#puts "Lord: "+get_member_name(lord)+", details: "+lord.inspect
 