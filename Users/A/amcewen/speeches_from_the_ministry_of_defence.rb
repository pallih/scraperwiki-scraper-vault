# Ruby scraper for mod.uk speeches
# TODO: map ministerial positions onto parlparse ids
require 'nokogiri'
require 'uri'
require 'mechanize'

BASE_URL = 'http://www.mod.uk/DefenceInternet/AboutDefence/People/Speeches/'
@parsed_base_url = URI.parse(BASE_URL)
Mechanize.html_parser = Nokogiri::HTML
@record_count = 0

def alternate_name(name)
  alternates = { 'chris' => 'christopher', 'greg' => 'gregory', 'nick' => 'nicholas', 'ed' => 'edward' }
  # And add the inverse alternatives
  alternates.each { |k, v| alternates[v] = k }
  # Return the alternative if it's available
  alternates[name.downcase]
end
  
# Function to search a list of members of parliament from parlparse, given the URL for the parlparse list
def build_members_from_url(url)
  # Retrieve a list of members of parliament from parlparse
  member_html = ScraperWiki.scrape(url)
  member_doc = Nokogiri::HTML(member_html)
  # Build a list of names for easy comparison
  member_doc.css('member').each do |m| 
    @members[m['firstname'].downcase+" "+m['lastname'].downcase] = m
    # See if there's an alternative name option (e.g. Christopher and Chris are synonyms)
    if alternate_name(m['firstname'])
      # Just add this as an extra value in the hash
      @members[alternate_name(m['firstname']).downcase+" "+m['lastname'].downcase] = m
    end
  end
end
  
# Function to search a list of lords from parlparse, given the URL for the parlparse list
def build_lords_from_url(url)
  # Retrieve a list of lords from parlparse
  lords_html = ScraperWiki.scrape(url)
  lords_doc = Nokogiri::HTML(lords_html)
  # Build a list of names for easy comparison
  @lords = {}
  lords_doc.css('lord').each do |l| 
    @lords[l['title'].downcase+" "+l['lordname'].downcase] = l
    unless l['forenames'].nil? 
      @lords[l['title'].downcase+" "+l['forenames'].downcase+" "+l['lordname'].downcase] = l
    end
  end
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
 
  member = @members[name.downcase]
  if member.nil? 
    member = @lords[name.downcase]
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

#### These functions are only needed if you don't get member names, but get ministerial positions instead
def get_ministers_from_parlparse
  # Retrieve a list of members of parliament from parlparse
  minister_html = ScraperWiki.scrape('http://ukparse.kforge.net/svn/parlparse/members/ministers.xml')
  @minister_doc = Nokogiri::HTML(minister_html)
end

def get_minister_name(dept, position, search_date)
  puts "Getting minister name. Dept: #{dept}; position: #{position}; date: #{search_date}"
  dept_shortnames = { "Ministry of Defence" => "Defence" }
   # See if we can find the given position
  minister_name = nil
  ministers = @minister_doc.css("moffice[dept='#{dept}'][position='#{position}']")
  if ministers.empty? 
    # We didn't get any matches, it could be because we're looking for "Secretary of State" for example,
    # when in the parlparse data that would be "Secretary of State for Defence", so try adding that
    dept_position = position+" for "+dept_shortnames[dept]
    ministers = @minister_doc.css("moffice[dept='#{dept}'][position='#{dept_position}']")
   end
  ministers.each do |m|
    begin
      start_date = Date.parse(m['fromdate'])
      end_date = Date.parse(m['todate'])
      search_date = Date.parse(search_date)
      if search_date >= start_date && search_date < end_date
        # We've found who we want
        minister_name = m['name']
      end
    rescue
    end
  end
  # If we haven't found one when we get here, it's probably because the parlparse data
  # only goes up to the last general election (or did as of 7/3/2011)
  # As a workaround, assume it's the current minister if we didn't find one in the parlparse data
  if minister_name.nil? 
    current_ministers = { "Under Secretary of State and the Lords Spokesman on Defence" => "Lord Astor",
                          "Minister for Defence Equipment, Support and Technology" => "Peter Luff",
                          "Minister for Defence Personnel, Welfare and Veterans" => "Andrew Robathan",
                          "Minister for International Security Strategy" => "Gerald Howarth",
                          "Minister of State for the Armed Forces" => "Nick Harvey",
                          "Secretary of State" => "Liam Fox" }
    minister_name = current_ministers[position]
  end
  minister_name
end
#### 
 
# Scrape a page of speech links to get the speeches
def scrape_speech_list(page_body)
  doc = Nokogiri::HTML(page_body)

  # Work out whose speeches we're scraping
  ministerial_position = doc.css('h1')[0].inner_text.gsub("Speeches", "").strip
 
  # And now scrape the speeches
  doc.css('div.story h3 a').each do |speech|
    record = {'permalink' => @parsed_base_url.merge(speech['href']).to_s, 'department' => 'Ministry of Defence' }
    @record_count = @record_count + 1
    puts "#{@record_count} Looking at #{speech.inner_text}"
    puts "=> "+record['permalink']
    the_actual_speech = @br.get(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech.body)
 
    record['title'] = the_speech_doc.css('meta[name="DC.title"]')[0]['content']
    record['given_on'] = the_speech_doc.css('meta[name="DC.date.created"]')[0]['content']

    # Work out who was minister at the time
    if ministerial_position.downcase == "chiefs of staff" || ministerial_position.downcase == "senior officials"
      # It wasn't one of the ministers, so just record the position
      record['minister_name'] = ministerial_position
    else
      who = get_minister_name(record['department'], ministerial_position, record['given_on'])
      member = find_member(who)
      unless member.nil? 
        record['minister_name'] = get_member_name(member)
        record['minister_parlparse_id'] = member['id']
      else
        raise "#### ERROR: Failed to get member name. Position: #{ministerial_position}; who: #{who}"
      end
    end

    # See if we can work out where the speech was given
    intro = the_speech_doc.css('span#Pagesummary1_Summary')[0].inner_text
    # This summary contains who gave the speech, where and when, but seem to always be of the form
    # "<who> at <where> on <when>"
    if intro.match(/.*\sat\s(.*)\son\s.*/i)
      record['where'] = intro.match(/.*\sat\s(.*)\son\s.*/i)[1].strip
    end
 
    divs = the_speech_doc.css('#left-column div').each do |d|
      if d['class'].nil? 
        # This will be the actual content (rather than an image div for example)
        record['body'] = d.css('p').collect { |para| para.to_s }.join("\n\n") 
      end
    end

    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end
  end
end

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_speech_list(page.body)
  page.form_with(:name => 'DynamicListPage') do |f|
    # See if we've got a "Next" submit field
    submit_button = f.button_with(:value => /next/i)
    if submit_button
      f.add_button_to_query(submit_button)
      page = f.submit()
      scrape_and_look_for_next_link(page)
    end
  end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

# Pull down the parlparse data first
@members = {}
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members.xml')
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members-2010.xml')
build_lords_from_url('http://ukparse.kforge.net/svn/parlparse/members/peers-ucl.xml')
get_ministers_from_parlparse

starting_url = BASE_URL
# Get the index page where we'll extract the list of pages of speeches
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}

index_page = @br.get(starting_url)
index_doc = Nokogiri::HTML(index_page.body)
 
speaker_links = index_doc.css('dt.LinkAndSummary a')
if speaker_links.empty? 
  raise "#### ERROR: Failed to find any speaker pages to scrape"
end
 
speaker_links.each do |link| 

  puts "Scraping speaker page for "+link.inner_text+" at "+link['href']
  page = @br.get(@parsed_base_url.merge(link['href']).to_s)
  # Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
  # you click on the 'next' link. We'll mimic this in the function above.

  # start scraping
  scrape_and_look_for_next_link(page)

end

# Ruby scraper for mod.uk speeches
# TODO: map ministerial positions onto parlparse ids
require 'nokogiri'
require 'uri'
require 'mechanize'

BASE_URL = 'http://www.mod.uk/DefenceInternet/AboutDefence/People/Speeches/'
@parsed_base_url = URI.parse(BASE_URL)
Mechanize.html_parser = Nokogiri::HTML
@record_count = 0

def alternate_name(name)
  alternates = { 'chris' => 'christopher', 'greg' => 'gregory', 'nick' => 'nicholas', 'ed' => 'edward' }
  # And add the inverse alternatives
  alternates.each { |k, v| alternates[v] = k }
  # Return the alternative if it's available
  alternates[name.downcase]
end
  
# Function to search a list of members of parliament from parlparse, given the URL for the parlparse list
def build_members_from_url(url)
  # Retrieve a list of members of parliament from parlparse
  member_html = ScraperWiki.scrape(url)
  member_doc = Nokogiri::HTML(member_html)
  # Build a list of names for easy comparison
  member_doc.css('member').each do |m| 
    @members[m['firstname'].downcase+" "+m['lastname'].downcase] = m
    # See if there's an alternative name option (e.g. Christopher and Chris are synonyms)
    if alternate_name(m['firstname'])
      # Just add this as an extra value in the hash
      @members[alternate_name(m['firstname']).downcase+" "+m['lastname'].downcase] = m
    end
  end
end
  
# Function to search a list of lords from parlparse, given the URL for the parlparse list
def build_lords_from_url(url)
  # Retrieve a list of lords from parlparse
  lords_html = ScraperWiki.scrape(url)
  lords_doc = Nokogiri::HTML(lords_html)
  # Build a list of names for easy comparison
  @lords = {}
  lords_doc.css('lord').each do |l| 
    @lords[l['title'].downcase+" "+l['lordname'].downcase] = l
    unless l['forenames'].nil? 
      @lords[l['title'].downcase+" "+l['forenames'].downcase+" "+l['lordname'].downcase] = l
    end
  end
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
 
  member = @members[name.downcase]
  if member.nil? 
    member = @lords[name.downcase]
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

#### These functions are only needed if you don't get member names, but get ministerial positions instead
def get_ministers_from_parlparse
  # Retrieve a list of members of parliament from parlparse
  minister_html = ScraperWiki.scrape('http://ukparse.kforge.net/svn/parlparse/members/ministers.xml')
  @minister_doc = Nokogiri::HTML(minister_html)
end

def get_minister_name(dept, position, search_date)
  puts "Getting minister name. Dept: #{dept}; position: #{position}; date: #{search_date}"
  dept_shortnames = { "Ministry of Defence" => "Defence" }
   # See if we can find the given position
  minister_name = nil
  ministers = @minister_doc.css("moffice[dept='#{dept}'][position='#{position}']")
  if ministers.empty? 
    # We didn't get any matches, it could be because we're looking for "Secretary of State" for example,
    # when in the parlparse data that would be "Secretary of State for Defence", so try adding that
    dept_position = position+" for "+dept_shortnames[dept]
    ministers = @minister_doc.css("moffice[dept='#{dept}'][position='#{dept_position}']")
   end
  ministers.each do |m|
    begin
      start_date = Date.parse(m['fromdate'])
      end_date = Date.parse(m['todate'])
      search_date = Date.parse(search_date)
      if search_date >= start_date && search_date < end_date
        # We've found who we want
        minister_name = m['name']
      end
    rescue
    end
  end
  # If we haven't found one when we get here, it's probably because the parlparse data
  # only goes up to the last general election (or did as of 7/3/2011)
  # As a workaround, assume it's the current minister if we didn't find one in the parlparse data
  if minister_name.nil? 
    current_ministers = { "Under Secretary of State and the Lords Spokesman on Defence" => "Lord Astor",
                          "Minister for Defence Equipment, Support and Technology" => "Peter Luff",
                          "Minister for Defence Personnel, Welfare and Veterans" => "Andrew Robathan",
                          "Minister for International Security Strategy" => "Gerald Howarth",
                          "Minister of State for the Armed Forces" => "Nick Harvey",
                          "Secretary of State" => "Liam Fox" }
    minister_name = current_ministers[position]
  end
  minister_name
end
#### 
 
# Scrape a page of speech links to get the speeches
def scrape_speech_list(page_body)
  doc = Nokogiri::HTML(page_body)

  # Work out whose speeches we're scraping
  ministerial_position = doc.css('h1')[0].inner_text.gsub("Speeches", "").strip
 
  # And now scrape the speeches
  doc.css('div.story h3 a').each do |speech|
    record = {'permalink' => @parsed_base_url.merge(speech['href']).to_s, 'department' => 'Ministry of Defence' }
    @record_count = @record_count + 1
    puts "#{@record_count} Looking at #{speech.inner_text}"
    puts "=> "+record['permalink']
    the_actual_speech = @br.get(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech.body)
 
    record['title'] = the_speech_doc.css('meta[name="DC.title"]')[0]['content']
    record['given_on'] = the_speech_doc.css('meta[name="DC.date.created"]')[0]['content']

    # Work out who was minister at the time
    if ministerial_position.downcase == "chiefs of staff" || ministerial_position.downcase == "senior officials"
      # It wasn't one of the ministers, so just record the position
      record['minister_name'] = ministerial_position
    else
      who = get_minister_name(record['department'], ministerial_position, record['given_on'])
      member = find_member(who)
      unless member.nil? 
        record['minister_name'] = get_member_name(member)
        record['minister_parlparse_id'] = member['id']
      else
        raise "#### ERROR: Failed to get member name. Position: #{ministerial_position}; who: #{who}"
      end
    end

    # See if we can work out where the speech was given
    intro = the_speech_doc.css('span#Pagesummary1_Summary')[0].inner_text
    # This summary contains who gave the speech, where and when, but seem to always be of the form
    # "<who> at <where> on <when>"
    if intro.match(/.*\sat\s(.*)\son\s.*/i)
      record['where'] = intro.match(/.*\sat\s(.*)\son\s.*/i)[1].strip
    end
 
    divs = the_speech_doc.css('#left-column div').each do |d|
      if d['class'].nil? 
        # This will be the actual content (rather than an image div for example)
        record['body'] = d.css('p').collect { |para| para.to_s }.join("\n\n") 
      end
    end

    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end
  end
end

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page)
  scrape_speech_list(page.body)
  page.form_with(:name => 'DynamicListPage') do |f|
    # See if we've got a "Next" submit field
    submit_button = f.button_with(:value => /next/i)
    if submit_button
      f.add_button_to_query(submit_button)
      page = f.submit()
      scrape_and_look_for_next_link(page)
    end
  end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

# Pull down the parlparse data first
@members = {}
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members.xml')
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members-2010.xml')
build_lords_from_url('http://ukparse.kforge.net/svn/parlparse/members/peers-ucl.xml')
get_ministers_from_parlparse

starting_url = BASE_URL
# Get the index page where we'll extract the list of pages of speeches
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}

index_page = @br.get(starting_url)
index_doc = Nokogiri::HTML(index_page.body)
 
speaker_links = index_doc.css('dt.LinkAndSummary a')
if speaker_links.empty? 
  raise "#### ERROR: Failed to find any speaker pages to scrape"
end
 
speaker_links.each do |link| 

  puts "Scraping speaker page for "+link.inner_text+" at "+link['href']
  page = @br.get(@parsed_base_url.merge(link['href']).to_s)
  # Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
  # you click on the 'next' link. We'll mimic this in the function above.

  # start scraping
  scrape_and_look_for_next_link(page)

end

