# Ruby scraper for defra.gov.uk speeches
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
base_url = "http://ww2.defra.gov.uk/news/category/speeches/"
starting_url = base_url

# Keep getting pages of results until we reach the end (i.e. a page without a ">>" link)
while !starting_url.nil? 
  puts "Getting "+starting_url
  parsed_base_url = URI.parse(starting_url)
  html = ScraperWiki.scrape(starting_url)
 
  doc = Nokogiri::HTML(html)
 
  # And now scrape the speeches
  doc.css('p.item a').each do |speech|
    record = {'permalink' => parsed_base_url.merge(speech['href']).to_s,
              'department' => 'Department for Environment Food and Rural Affairs'}
    puts "Looking at #{speech.inner_text}"
    puts "=> "+record['permalink']
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

    record['title'] = the_speech_doc.css('h1.mainblock')[0].inner_text
    # See if there's a date in the title
    begin
      record['given_on'] = Date.parse(record['title']).to_s
    rescue
      # Can't find a date in the title, so use the 
      record['given_on'] = Date.parse(the_speech_doc.css('p.posttime')[0].inner_text)
    end

    # If the parlparse ministers.xml was more up-to-date, then we could possibly do something more intelligent here
    # For now, just search for any of the ministers from this list
    ministers = { "caroline spelman" => "caroline spelman", "spelman" => "caroline spelman", "jim paice" => "jim paice",
                  "paice" => "jim paice", "richard benyon" => "richard benyon", "benyon" => "richard benyon",
                  "lord henley" => "lord henley", "henley" => "lord henley" }
    ministers.each do |short, full|
      if record['title'].downcase.match(short)
        # We've found the speaker
        member = find_member(full)
        if member.nil? 
          raise "#### ERROR: Couldn't find member details for #{full}"
        else
          record['minister_name'] = get_member_name(member)
          record['minister_parlparse_id'] = member['id']
        end
        break
      end
    end

    record['body'] = the_speech_doc.css('#thecontent').inner_html 
    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end
  end

  # Get the next page of results
  if doc.css('.wp-paginate a.next').empty? 
    # We've reached the end of the results
    starting_url = nil
  else
    # Get the next page of results
    starting_url = parsed_base_url.merge(doc.css('.wp-paginate a.next')[0]['href']).to_s
  end
end

