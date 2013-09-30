# Ruby scraper for DECC.gov.uk speeches
require 'nokogiri'
require 'uri'

def alternate_name(name)
  alternates = { 'chris' => 'christopher', 'greg' => 'gregory', 'ed' => 'edward' }
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
  end
  lords[name.downcase]
end
 
# Function to map a given name to a parlparse member
# Returns either an MP or a Lord - these have different attributes, unfortunately, but both have an 'id'
def find_member(name)
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
base_url = "http://www.decc.gov.uk/en/news/"
starting_url = base_url
parsed_base_url = URI.parse(starting_url)
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

# Find all the speech categories from the menu on the left
speech_pages = []
doc.css('.category a').each do |category|
  if category.inner_text.match(/speeches/)
    speech_pages.push(parsed_base_url.merge(category['href']).to_s)
  end
end
if speech_pages.empty? 
  raise "#### ERROR: Couldn't find any pages of speeches"
end

# Now get all the speeches on each speech page
speech_pages.each do |category_url|

  html = ScraperWiki.scrape(category_url)
  doc = Nokogiri::HTML(html)

  # Find the links to the pages of results
  pages = []
  doc.css('.pagelinks>a').each do |pagelink|
    if pagelink['class'][0..9] == 'paginglink'
      # This is one of the links we're interested in (i.e. not a prev/next link)
      pages.push(pagelink['href'])
    end
  end

  pages.each do |page_url|

    starting_url = parsed_base_url.merge(page_url).to_s
    html = ScraperWiki.scrape(starting_url)
    doc = Nokogiri::HTML(html)

    # Work out whose speeches these are
    name = doc.css('.searchterm').inner_text.gsub(/speeches/, "").strip
    member = find_member(name)
    if member.nil? 
      raise "#### ERROR: Couldn't find member with name #{name}"
    end
    puts "Processing the speeches given by #{name}"

    # And now scrape the speeches
    doc.css('ol.search-results li').each do |li|
      record = {'title' => li.at('strong').inner_text.strip, 'permalink' => parsed_base_url.merge(li.at('a')['href']).to_s,
                'given_on' => li.css('span')[1].inner_text, 'minister_name' => get_member_name(member),
                'minister_parlparse_id' => member['id'], 'department' => 'Department for Energy and Climate Change'}
      puts "Looking at #{record['title']}"
      puts "=> "+record['permalink']
      the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
      the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

      #record['where'] = the_speech_doc.search('#Page>table tr td').last.text.strip
      if !the_speech_doc.css('.cms-text').empty? 
        # Sometimes, but not always, there'll be more than one "<div class='cms-text'>" element, and we'll just want the last one
        record['body'] = the_speech_doc.css('.cms-text').last.css('p').collect { |para| para.to_s }.join("\n\n") 
      elsif !the_speech_doc.css('.cms-textandimage').empty? 
        record['body'] = the_speech_doc.css('.cms-textandimage').last.css('p').collect { |para| para.to_s }.join("\n\n")
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

end
# Ruby scraper for DECC.gov.uk speeches
require 'nokogiri'
require 'uri'

def alternate_name(name)
  alternates = { 'chris' => 'christopher', 'greg' => 'gregory', 'ed' => 'edward' }
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
  end
  lords[name.downcase]
end
 
# Function to map a given name to a parlparse member
# Returns either an MP or a Lord - these have different attributes, unfortunately, but both have an 'id'
def find_member(name)
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
base_url = "http://www.decc.gov.uk/en/news/"
starting_url = base_url
parsed_base_url = URI.parse(starting_url)
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

# Find all the speech categories from the menu on the left
speech_pages = []
doc.css('.category a').each do |category|
  if category.inner_text.match(/speeches/)
    speech_pages.push(parsed_base_url.merge(category['href']).to_s)
  end
end
if speech_pages.empty? 
  raise "#### ERROR: Couldn't find any pages of speeches"
end

# Now get all the speeches on each speech page
speech_pages.each do |category_url|

  html = ScraperWiki.scrape(category_url)
  doc = Nokogiri::HTML(html)

  # Find the links to the pages of results
  pages = []
  doc.css('.pagelinks>a').each do |pagelink|
    if pagelink['class'][0..9] == 'paginglink'
      # This is one of the links we're interested in (i.e. not a prev/next link)
      pages.push(pagelink['href'])
    end
  end

  pages.each do |page_url|

    starting_url = parsed_base_url.merge(page_url).to_s
    html = ScraperWiki.scrape(starting_url)
    doc = Nokogiri::HTML(html)

    # Work out whose speeches these are
    name = doc.css('.searchterm').inner_text.gsub(/speeches/, "").strip
    member = find_member(name)
    if member.nil? 
      raise "#### ERROR: Couldn't find member with name #{name}"
    end
    puts "Processing the speeches given by #{name}"

    # And now scrape the speeches
    doc.css('ol.search-results li').each do |li|
      record = {'title' => li.at('strong').inner_text.strip, 'permalink' => parsed_base_url.merge(li.at('a')['href']).to_s,
                'given_on' => li.css('span')[1].inner_text, 'minister_name' => get_member_name(member),
                'minister_parlparse_id' => member['id'], 'department' => 'Department for Energy and Climate Change'}
      puts "Looking at #{record['title']}"
      puts "=> "+record['permalink']
      the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
      the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

      #record['where'] = the_speech_doc.search('#Page>table tr td').last.text.strip
      if !the_speech_doc.css('.cms-text').empty? 
        # Sometimes, but not always, there'll be more than one "<div class='cms-text'>" element, and we'll just want the last one
        record['body'] = the_speech_doc.css('.cms-text').last.css('p').collect { |para| para.to_s }.join("\n\n") 
      elsif !the_speech_doc.css('.cms-textandimage').empty? 
        record['body'] = the_speech_doc.css('.cms-textandimage').last.css('p').collect { |para| para.to_s }.join("\n\n")
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

end
