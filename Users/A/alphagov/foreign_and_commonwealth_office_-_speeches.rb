# Ruby scraper for FCO.gov.uk speeches
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
    unless l['lordofname'].nil? 
      @lords[l['title'].downcase+" "+l['lordname'].downcase+" of "+l['lordofname'].downcase] = l
      unless l['forenames'].nil? 
        @lords[l['title'].downcase+" "+l['forenames'].downcase+" "+l['lordname'].downcase+" of "+l['lordofname'].downcase] = l
      end
    end
  end
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
  name.gsub!("the foreign secretary", "")
  name.gsub!("foreign secretary", "")
  name.gsub!("foreign office minister", "")
  name.gsub!("international development minister", "")
  name.gsub!("minister for trade & investment", "")
  name.gsub!("uk minister for europe", "")
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

@record_count = 0

# Pull down the parlparse data first
@members = {}
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members.xml')
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members-2010.xml')
build_lords_from_url('http://ukparse.kforge.net/svn/parlparse/members/peers-ucl.xml')

# retrieve the news index page
base_url = "http://www.fco.gov.uk/en/news/speeches-and-transcripts/speeches/"
starting_url = base_url

# Keep getting pages of results until we reach the end (i.e. a page without a "Next" link)
while !starting_url.nil? 
  puts "Getting "+starting_url
  parsed_base_url = URI.parse(starting_url)
  html = ScraperWiki.scrape(starting_url)
 
  doc = Nokogiri::HTML(html)
 
  # And now scrape the speeches
  doc.css('h3.NewsHeadline a').each do |speech|
    record = {'permalink' => parsed_base_url.merge(speech['href']).to_s,
              'department' => 'Foreign and Commonwealth Office'}
    @record_count = @record_count + 1
    puts "#{@record_count} Looking at #{speech.inner_text}"
    puts "=> "+record['permalink']
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

    record['title'] = the_speech_doc.css('meta[name="DC.title"]')[0]['content']
    record['given_on'] = the_speech_doc.css('.NewsHeader p.Smaller').inner_text.strip

    the_speech_doc.css('table.SpeachDetails tr').each do |detail_row|
      if detail_row.css('td')[0].inner_text.match(/speaker/i)
        # This row has the speaker's name
        name = detail_row.css('td')[1].inner_text.strip
        member = find_member(name)
        if member.nil? 
          non_member_speakers = ["John Ashton", "Sir John Sawers", "Bob Dewar, British High Commssioner to Nigeria",
                                 "Pope Benedict XVI", "Her Majesty the Queen", "Mr Matthew Johnson"]
          if non_member_speakers.include?(name)
            # It's one of the few non-MP/Lord speakers
            record['minister_name'] = name
          else
            raise "#### ERROR: Couldn't find member details for #{name}"
          end
        else
          record['minister_name'] = get_member_name(member)
          record['minister_parlparse_id'] = member['id']
        end
      end
      if detail_row.css('td')[0].inner_text.match(/location/i)
        # This row has where the speech was given
        record['where'] = detail_row.css('td')[1].inner_text.strip
      end
    end

    # In <div id="Main">, after <table> and before <h3>, collect the contents of all the <p> elements
    skipped_header = false
    reached_footer = false
    speech_paras = []
    the_speech_doc.css('#Main')[0].children.each do |e|
      if !skipped_header
        if !e['class'].nil? && e['class'].match(/NewsHeader/i)
          # This is the header element, so everything after will be the content
          skipped_header = true
        end
      else
        if !reached_footer
          if e.name == "h3"
            # We've hit the "more information" area, and so the end of the speech
            reached_footer = true
          elsif e.name == "p"
            # Collect any paragraph elements, as they're from the speech content
            speech_paras.push(e)
          end
        end
      end
    end

    unless speech_paras.empty? 
      record['body'] = speech_paras.collect { |para| para.to_s }.join("\n\n") 
    else
      raise "#### ERROR: FAILED TO FIND THE SPEECH"
    end
    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end
  end

  # Get the next page of results
  if doc.css('a.OtherResultsPage[title~="Next"]').empty? 
    # We've reached the end of the results
    starting_url = nil
  else
    # Get the next page of results
    starting_url = parsed_base_url.merge(doc.css('a.OtherResultsPage[title~="Next"]')[0]['href']).to_s
  end
end

# Ruby scraper for FCO.gov.uk speeches
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
    unless l['lordofname'].nil? 
      @lords[l['title'].downcase+" "+l['lordname'].downcase+" of "+l['lordofname'].downcase] = l
      unless l['forenames'].nil? 
        @lords[l['title'].downcase+" "+l['forenames'].downcase+" "+l['lordname'].downcase+" of "+l['lordofname'].downcase] = l
      end
    end
  end
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
  name.gsub!("the foreign secretary", "")
  name.gsub!("foreign secretary", "")
  name.gsub!("foreign office minister", "")
  name.gsub!("international development minister", "")
  name.gsub!("minister for trade & investment", "")
  name.gsub!("uk minister for europe", "")
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

@record_count = 0

# Pull down the parlparse data first
@members = {}
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members.xml')
build_members_from_url('http://ukparse.kforge.net/svn/parlparse/members/all-members-2010.xml')
build_lords_from_url('http://ukparse.kforge.net/svn/parlparse/members/peers-ucl.xml')

# retrieve the news index page
base_url = "http://www.fco.gov.uk/en/news/speeches-and-transcripts/speeches/"
starting_url = base_url

# Keep getting pages of results until we reach the end (i.e. a page without a "Next" link)
while !starting_url.nil? 
  puts "Getting "+starting_url
  parsed_base_url = URI.parse(starting_url)
  html = ScraperWiki.scrape(starting_url)
 
  doc = Nokogiri::HTML(html)
 
  # And now scrape the speeches
  doc.css('h3.NewsHeadline a').each do |speech|
    record = {'permalink' => parsed_base_url.merge(speech['href']).to_s,
              'department' => 'Foreign and Commonwealth Office'}
    @record_count = @record_count + 1
    puts "#{@record_count} Looking at #{speech.inner_text}"
    puts "=> "+record['permalink']
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

    record['title'] = the_speech_doc.css('meta[name="DC.title"]')[0]['content']
    record['given_on'] = the_speech_doc.css('.NewsHeader p.Smaller').inner_text.strip

    the_speech_doc.css('table.SpeachDetails tr').each do |detail_row|
      if detail_row.css('td')[0].inner_text.match(/speaker/i)
        # This row has the speaker's name
        name = detail_row.css('td')[1].inner_text.strip
        member = find_member(name)
        if member.nil? 
          non_member_speakers = ["John Ashton", "Sir John Sawers", "Bob Dewar, British High Commssioner to Nigeria",
                                 "Pope Benedict XVI", "Her Majesty the Queen", "Mr Matthew Johnson"]
          if non_member_speakers.include?(name)
            # It's one of the few non-MP/Lord speakers
            record['minister_name'] = name
          else
            raise "#### ERROR: Couldn't find member details for #{name}"
          end
        else
          record['minister_name'] = get_member_name(member)
          record['minister_parlparse_id'] = member['id']
        end
      end
      if detail_row.css('td')[0].inner_text.match(/location/i)
        # This row has where the speech was given
        record['where'] = detail_row.css('td')[1].inner_text.strip
      end
    end

    # In <div id="Main">, after <table> and before <h3>, collect the contents of all the <p> elements
    skipped_header = false
    reached_footer = false
    speech_paras = []
    the_speech_doc.css('#Main')[0].children.each do |e|
      if !skipped_header
        if !e['class'].nil? && e['class'].match(/NewsHeader/i)
          # This is the header element, so everything after will be the content
          skipped_header = true
        end
      else
        if !reached_footer
          if e.name == "h3"
            # We've hit the "more information" area, and so the end of the speech
            reached_footer = true
          elsif e.name == "p"
            # Collect any paragraph elements, as they're from the speech content
            speech_paras.push(e)
          end
        end
      end
    end

    unless speech_paras.empty? 
      record['body'] = speech_paras.collect { |para| para.to_s }.join("\n\n") 
    else
      raise "#### ERROR: FAILED TO FIND THE SPEECH"
    end
    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end
  end

  # Get the next page of results
  if doc.css('a.OtherResultsPage[title~="Next"]').empty? 
    # We've reached the end of the results
    starting_url = nil
  else
    # Get the next page of results
    starting_url = parsed_base_url.merge(doc.css('a.OtherResultsPage[title~="Next"]')[0]['href']).to_s
  end
end

