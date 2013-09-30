require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

MAX_KEY_LENGTH = 10

class Fixnum
  def ordinal
    # teens
    return 'th' if (10..19).include?(self % 100)
    # others
    case self % 10
    when 1
     'st'
    when 2
      'nd'
    when 3
      'rd'
    else
      'th'
    end
  end
end

def metadata_key(i)
  "#{i}#{i.ordinal}_letter"
end

def reset_metadata(from)
  from.upto(MAX_KEY_LENGTH).each do |i|
    save_metadata(metadata_key(i), CHARS.first)
  end
end

def get_metadata(key, default)
  ScraperWiki.get_metadata(key, default)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  retry
end

def save_metadata(key, value)
  ScraperWiki.save_metadata(key, value)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
  retry
end

def submit(page)
  page.forms[0].submit
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during submit\n#{page.forms[0].fields.map{|x| "#{x.name} = #{x.value}"}.join("\n") }"
  retry
end

def download(prefix)
  agent = Mechanize.new
  agent.user_agent_alias = 'Mac Safari'
  page = agent.get 'http://nvsos.gov/sosentitysearch/corpsearch.aspx'

  page.forms[0]['ctl00$MainContent$ddlCorpSortColumns'] = 'b'
  page.forms[0]['ctl00$MainContent$rdlSortOrder'] = 'd'
  page.forms[0]['ctl00$MainContent$btnCorpSearch'] = 'Search'
  page.forms[0]['ctl00$MainContent$txtSearchBox'] = prefix
  page = submit(page)
  num_results = page.parser.at_css('#ctl00_MainContent_objSearchGrid_lblMessage').text[/(\d+) search results/, 1].to_i

  if num_results.zero? 
    puts "No records for #{prefix}"
  elsif num_results >= 500
    key = metadata_key(prefix.size + 1)
    initial = get_metadata(key, CHARS.first)
    CHARS[CHARS.index(initial)..-1].each do |c|
      save_metadata(key, c)
      download prefix + c
    end
    reset_metadata(prefix.size + 1)
  else
    puts "#{num_results} records for #{prefix}"
    extract page
  end
end

def extract(page)
  prefix = page.forms[0]['ctl00$MainContent$txtSearchBox']
  total_pages = page.parser.css('#ctl00_MainContent_objSearchGrid_dgCorpSearchResults tr:not([class]) a').size + 1
  page_number = page.parser.at_css('#ctl00_MainContent_objSearchGrid_dgCorpSearchResults tr:not([class]) span').text.to_i

  puts "Scraping #{prefix} page #{page_number}/#{total_pages}"

  page.parser.css('#ctl00_MainContent_objSearchGrid_dgCorpSearchResults .TDColorC').each do |tr|
    entity_type = tr.at_css('td:eq(4)').text.strip
    next if entity_type == 'Reserved Name'

    a = tr.at_css('td:eq(2) a')
    record = {
      'CompanyNumber' => a.text.strip,
      'RegistryUrl'   => 'http://nvsos.gov/sosentitysearch/' + a[:href],
      'CompanyName'   => tr.at_css('td:eq(1)').text.strip,
      'Status'        => tr.at_css('td:eq(3)').text.strip,
      'EntityType'    => entity_type,
    }

    begin
      ScraperWiki.save(['CompanyNumber'], record)
    rescue Timeout::Error => e
      puts "ERROR: #{e.inspect} during save(#{record.inspect})"
      retry
    end
  end

  # Advance to the next page, or reset.
  if page_number < total_pages
    page.forms[0]['__EVENTTARGET'] = "ctl00$MainContent$objSearchGrid$dgCorpSearchResults$ctl54$ctl#{'%02d' % page_number}"
    extract submit(page)
  end
end


Mechanize.html_parser = Nokogiri::HTML
CHARS = [*'0'..'9'] + [*'A'..'Z']

initial = {}
1.upto(MAX_KEY_LENGTH).each do |i|
  initial[i] = get_metadata(metadata_key(i), CHARS.first)
end

# "zzz" returns fewer than 500 results, so no need to worry about 4th+ letters.
if initial[1] == CHARS.last && initial[2] == CHARS.last && initial[3] == CHARS.last
  1.upto(MAX_KEY_LENGTH).each do |i|
    initial[i] = CHARS.first
    save_metadata(metadata_key(i), initial[i])
  end
end

puts "Initial prefix is #{initial.sort_by{|i,letter| i}.reduce(''){|memo,(i,letter)| memo + letter}.sub(/!+\Z/, '')}"

CHARS[CHARS.index(initial[1])..-1].each do |a|
  save_metadata(metadata_key(1), a)
  download(a)
end

require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

MAX_KEY_LENGTH = 10

class Fixnum
  def ordinal
    # teens
    return 'th' if (10..19).include?(self % 100)
    # others
    case self % 10
    when 1
     'st'
    when 2
      'nd'
    when 3
      'rd'
    else
      'th'
    end
  end
end

def metadata_key(i)
  "#{i}#{i.ordinal}_letter"
end

def reset_metadata(from)
  from.upto(MAX_KEY_LENGTH).each do |i|
    save_metadata(metadata_key(i), CHARS.first)
  end
end

def get_metadata(key, default)
  ScraperWiki.get_metadata(key, default)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  retry
end

def save_metadata(key, value)
  ScraperWiki.save_metadata(key, value)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
  retry
end

def submit(page)
  page.forms[0].submit
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during submit\n#{page.forms[0].fields.map{|x| "#{x.name} = #{x.value}"}.join("\n") }"
  retry
end

def download(prefix)
  agent = Mechanize.new
  agent.user_agent_alias = 'Mac Safari'
  page = agent.get 'http://nvsos.gov/sosentitysearch/corpsearch.aspx'

  page.forms[0]['ctl00$MainContent$ddlCorpSortColumns'] = 'b'
  page.forms[0]['ctl00$MainContent$rdlSortOrder'] = 'd'
  page.forms[0]['ctl00$MainContent$btnCorpSearch'] = 'Search'
  page.forms[0]['ctl00$MainContent$txtSearchBox'] = prefix
  page = submit(page)
  num_results = page.parser.at_css('#ctl00_MainContent_objSearchGrid_lblMessage').text[/(\d+) search results/, 1].to_i

  if num_results.zero? 
    puts "No records for #{prefix}"
  elsif num_results >= 500
    key = metadata_key(prefix.size + 1)
    initial = get_metadata(key, CHARS.first)
    CHARS[CHARS.index(initial)..-1].each do |c|
      save_metadata(key, c)
      download prefix + c
    end
    reset_metadata(prefix.size + 1)
  else
    puts "#{num_results} records for #{prefix}"
    extract page
  end
end

def extract(page)
  prefix = page.forms[0]['ctl00$MainContent$txtSearchBox']
  total_pages = page.parser.css('#ctl00_MainContent_objSearchGrid_dgCorpSearchResults tr:not([class]) a').size + 1
  page_number = page.parser.at_css('#ctl00_MainContent_objSearchGrid_dgCorpSearchResults tr:not([class]) span').text.to_i

  puts "Scraping #{prefix} page #{page_number}/#{total_pages}"

  page.parser.css('#ctl00_MainContent_objSearchGrid_dgCorpSearchResults .TDColorC').each do |tr|
    entity_type = tr.at_css('td:eq(4)').text.strip
    next if entity_type == 'Reserved Name'

    a = tr.at_css('td:eq(2) a')
    record = {
      'CompanyNumber' => a.text.strip,
      'RegistryUrl'   => 'http://nvsos.gov/sosentitysearch/' + a[:href],
      'CompanyName'   => tr.at_css('td:eq(1)').text.strip,
      'Status'        => tr.at_css('td:eq(3)').text.strip,
      'EntityType'    => entity_type,
    }

    begin
      ScraperWiki.save(['CompanyNumber'], record)
    rescue Timeout::Error => e
      puts "ERROR: #{e.inspect} during save(#{record.inspect})"
      retry
    end
  end

  # Advance to the next page, or reset.
  if page_number < total_pages
    page.forms[0]['__EVENTTARGET'] = "ctl00$MainContent$objSearchGrid$dgCorpSearchResults$ctl54$ctl#{'%02d' % page_number}"
    extract submit(page)
  end
end


Mechanize.html_parser = Nokogiri::HTML
CHARS = [*'0'..'9'] + [*'A'..'Z']

initial = {}
1.upto(MAX_KEY_LENGTH).each do |i|
  initial[i] = get_metadata(metadata_key(i), CHARS.first)
end

# "zzz" returns fewer than 500 results, so no need to worry about 4th+ letters.
if initial[1] == CHARS.last && initial[2] == CHARS.last && initial[3] == CHARS.last
  1.upto(MAX_KEY_LENGTH).each do |i|
    initial[i] = CHARS.first
    save_metadata(metadata_key(i), initial[i])
  end
end

puts "Initial prefix is #{initial.sort_by{|i,letter| i}.reduce(''){|memo,(i,letter)| memo + letter}.sub(/!+\Z/, '')}"

CHARS[CHARS.index(initial[1])..-1].each do |a|
  save_metadata(metadata_key(1), a)
  download(a)
end

