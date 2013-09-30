# Ruby scraper for culture.gov.uk speeches
require 'nokogiri'
require 'uri'
require 'mechanize'

BASE_URL = 'http://www.culture.gov.uk/news/ministers_speeches/'
@parsed_base_url = URI.parse(BASE_URL)
Mechanize.html_parser = Nokogiri::HTML

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
 
# Scrape a page of speech links to get the speeches
def scrape_speech_list(page_body)
  doc = Nokogiri::HTML(page_body)

  # Work out whose speeches we're scraping
  name = doc.css('h1')[0].inner_text.strip
  member = find_member(name) 
  if member.nil? 
    raise "#### ERROR: Failed to find member #{name}"
  end
 
  # And now scrape the speeches
  doc.css('div.ArticleDetail h2 a').each do |speech|
    record = {'permalink' => @parsed_base_url.merge(speech['href']).to_s, 'minister_name' => get_member_name(member),
              'minister_parlparse_id' => member['id'], 'department' => 'Department for Culture Media and Sport'}
    puts "Looking at #{speech.inner_text}"
    puts "=> "+record['permalink']
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)
 
    record['title'] = the_speech_doc.css('meta[name="DC.title"]')[0]['content'].gsub('Department for Culture Media and Sport - ', '')
    record['given_on'] = the_speech_doc.css('meta[name="APR_Date"]')[0]['content']

    # See if we can work out where the speech was given
    intro = the_speech_doc.css('.introtext p')[0].inner_html
    # The first <p> element contains the date, and also sometimes the location, but not in a fixed order, sometimes
    # they're separated by a ',' and sometimes by '<br>' or '<br />'
    intro_elements = []
    if intro.match(/<br.*>/)
      # Split by <br> elements
      intro_elements = intro.match(/(.*)<br.*>(.*)/).to_a
      intro_elements.delete_at(0)
    else
      intro_elements = intro.split(',')
    end
    begin
      # If this parses successfully, then it's date first
      Date.parse(intro_elements[0])
      record['where'] = intro_elements[1]
    rescue
      # The first element isn't a date, we'll assume it's a location
      record['where'] = intro_elements[0]
    end
 
    paragraphs = the_speech_doc.css('#contentcolumn p').to_a
    paragraphs.reject! { |p| p.css('a').inner_text.match(/back to/i) }

    unless paragraphs.empty? 
      record['body'] = paragraphs.collect { |para| para.to_s }.join("\n\n") 
    else
      puts the_speech_doc.inspect
      raise "#### ERROR: FAILED TO FIND THE SPEECH"
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
    link = page.link_with(:text => 'Next >')
    if link
      page.form_with(:name => 'form1') do |f|
        f['__EVENTTARGET'] = 'ctl01$listing$ctl00$pager$nextButton'
        f['__EVENTARGUMENT'] = ''
        page = f.submit()
      end
    scrape_and_look_for_next_link(page)
    end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = BASE_URL
# Get the index page where we'll extract the list of pages of speeches
index_html = ScraperWiki.scrape(starting_url)
index_doc = Nokogiri::HTML(index_html)

speaker_links = index_doc.css('#leftnav ul ul ul li a')
if speaker_links.empty? 
  raise "#### ERROR: Failed to find any speaker pages to scrape"
end

speaker_links.each do |link|

  @br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
    browser.user_agent_alias = 'Linux Firefox'
  }
  puts "Scraping speaker page for "+link.inner_text+" at "+link['href']
  page = @br.get(@parsed_base_url.merge(link['href']).to_s)
  # Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
  # you click on the 'next' link. We'll mimic this in the function above.

  # start scraping
  scrape_and_look_for_next_link(page)

end
# Ruby scraper for culture.gov.uk speeches
require 'nokogiri'
require 'uri'
require 'mechanize'

BASE_URL = 'http://www.culture.gov.uk/news/ministers_speeches/'
@parsed_base_url = URI.parse(BASE_URL)
Mechanize.html_parser = Nokogiri::HTML

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
 
# Scrape a page of speech links to get the speeches
def scrape_speech_list(page_body)
  doc = Nokogiri::HTML(page_body)

  # Work out whose speeches we're scraping
  name = doc.css('h1')[0].inner_text.strip
  member = find_member(name) 
  if member.nil? 
    raise "#### ERROR: Failed to find member #{name}"
  end
 
  # And now scrape the speeches
  doc.css('div.ArticleDetail h2 a').each do |speech|
    record = {'permalink' => @parsed_base_url.merge(speech['href']).to_s, 'minister_name' => get_member_name(member),
              'minister_parlparse_id' => member['id'], 'department' => 'Department for Culture Media and Sport'}
    puts "Looking at #{speech.inner_text}"
    puts "=> "+record['permalink']
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)
 
    record['title'] = the_speech_doc.css('meta[name="DC.title"]')[0]['content'].gsub('Department for Culture Media and Sport - ', '')
    record['given_on'] = the_speech_doc.css('meta[name="APR_Date"]')[0]['content']

    # See if we can work out where the speech was given
    intro = the_speech_doc.css('.introtext p')[0].inner_html
    # The first <p> element contains the date, and also sometimes the location, but not in a fixed order, sometimes
    # they're separated by a ',' and sometimes by '<br>' or '<br />'
    intro_elements = []
    if intro.match(/<br.*>/)
      # Split by <br> elements
      intro_elements = intro.match(/(.*)<br.*>(.*)/).to_a
      intro_elements.delete_at(0)
    else
      intro_elements = intro.split(',')
    end
    begin
      # If this parses successfully, then it's date first
      Date.parse(intro_elements[0])
      record['where'] = intro_elements[1]
    rescue
      # The first element isn't a date, we'll assume it's a location
      record['where'] = intro_elements[0]
    end
 
    paragraphs = the_speech_doc.css('#contentcolumn p').to_a
    paragraphs.reject! { |p| p.css('a').inner_text.match(/back to/i) }

    unless paragraphs.empty? 
      record['body'] = paragraphs.collect { |para| para.to_s }.join("\n\n") 
    else
      puts the_speech_doc.inspect
      raise "#### ERROR: FAILED TO FIND THE SPEECH"
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
    link = page.link_with(:text => 'Next >')
    if link
      page.form_with(:name => 'form1') do |f|
        f['__EVENTTARGET'] = 'ctl01$listing$ctl00$pager$nextButton'
        f['__EVENTARGUMENT'] = ''
        page = f.submit()
      end
    scrape_and_look_for_next_link(page)
    end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

starting_url = BASE_URL
# Get the index page where we'll extract the list of pages of speeches
index_html = ScraperWiki.scrape(starting_url)
index_doc = Nokogiri::HTML(index_html)

speaker_links = index_doc.css('#leftnav ul ul ul li a')
if speaker_links.empty? 
  raise "#### ERROR: Failed to find any speaker pages to scrape"
end

speaker_links.each do |link|

  @br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
    browser.user_agent_alias = 'Linux Firefox'
  }
  puts "Scraping speaker page for "+link.inner_text+" at "+link['href']
  page = @br.get(@parsed_base_url.merge(link['href']).to_s)
  # Have a look at 'page': note the 'onSubmit' JavaScript function that is called when 
  # you click on the 'next' link. We'll mimic this in the function above.

  # start scraping
  scrape_and_look_for_next_link(page)

end
