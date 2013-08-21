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

def download(prefix)
  # Can't use open-uri, as we must have cookies set for pagination.
  agent = Mechanize.new do |b|
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  end

  begin
    page = agent.get("#{BASE_URL}/NASApp/tmf/TMFServlet?app=MYBIZFILE-DIR-ENTITY&searchText=#{CGI.escape(prefix)}&searchBy=name")
  rescue Timeout::Error => e
    puts "ERROR: #{e.inspect} during download(#{prefix})"
    retry
  end

  if page.body.match(/No record found/)
    puts "No records for #{prefix}"
    return prefix.match(/_\Z/) # do not iterate if using wildcard
  elsif page.body.match(/Invalid character found in the search criteria\./)
    puts "WARNING: Invalid character in #{prefix}"
    return prefix.match(/_\Z/) # do not iterate if using wildcard
  elsif page.body.match(/More than 500 records found\. Please refine your search\. Currently you can only view 500 records\./)
    if prefix.match /_\Z/ # _ is a wildcard
      return !prefix.match(/_\Z/) # iterate if using wildcard
    else
      key = metadata_key(prefix.size + 1)
      initial = get_metadata(key, CHARS.first)
      CHARS[CHARS.index(initial)..-1].each do |c|
        save_metadata(key, c)
        download prefix + c
      end
      reset_metadata(prefix.size + 1)
    end
  else
    paths = page.parser.css('td.tdright[colspan="2"] a').map{|a| a[:href]}

    pageno = 1
    puts "Companies starting with #{prefix}, page #{pageno}/#{paths.size + 1}"
    extract(page.parser)

    paths.each do |path|
      begin
        page = agent.get(BASE_URL + path)
      rescue Timeout::Error => e
        puts "ERROR: #{e.inspect} during download(#{prefix})"
        retry
      end

      pageno += 1
      puts "Companies starting with #{prefix}, page #{pageno}/#{paths.size + 1}"
      extract(page.parser)
    end

    return prefix.match(/_\Z/) # do not iterate if using wildcard
  end
end

def extract(doc)
  doc.css('tr.tdleft').each do |tr|
    # The company number is sometimes suffixed. If the number begins with "T",
    # it has a suffix like "(LL0601237K)". If "N", then "(App No.)". If "S",
    # then "(F   04692H)". I maintain these in case they are meaningful.
    full_number = tr.at_css('td:eq(2)').text.gsub(/[[:space:]]/, ' ').strip

    # The site breaks on company names containing quotation marks.
    if full_number.match />|\(/
      number = full_number.sub(/.+>/,'')[/^(\w+)/,1]
    else
      number = full_number
    end

    rating = if tr.at_css('td:eq(6) img[width="32"]')
      'Y'
    elsif tr.at_css('td:eq(6) img[width="28"]')
      'N'
    elsif tr.at_css('td:eq(6)').text == '-'
      'N/A'
    else
      puts "WARNING: Unknown compliance rating: #{tr.at_css('td:eq(6)').text}"
    end
    raw = tr.at_css('td:eq(3)').text.gsub(/[[:space:]]/, ' ').strip
    record = {
      'CompanyNumber'    => number,
      'FullCompanyNumber'=> full_number.strip,
      'RegistryUrl'      => BASE_URL + tr.at_css('td:eq(2) a')[:href].gsub(/[[:space:]]/, ' ').strip,
      'RawName'          => raw,
      # raw[/ n\.k\.a /] ? raw[/ n\.k\.a (.+?)(?: f.k.a .+)?\Z/, 1] : raw[/^(.+?)(?: f\.k\.a .+)?\Z/, 1],
      'CompanyName'      => raw[/^(.+?)(?: [nf]\.k\.a .+)?\Z/, 1],
      'PartialAddress'   => tr.at_css('td:eq(4)').text.gsub(/[[:space:]]/, ' ').strip,
      'Status'           => tr.at_css('td:eq(5)').text.gsub(/[[:space:]]/, ' ').strip,
      'ComplianceRating' => rating,
      'DateScraped'      => Time.now
    }
    begin
      ScraperWiki.save(['CompanyNumber'], record)
    rescue Timeout::Error => e
      puts "ERROR: #{e.inspect} during save(#{record.inspect})"
      retry
    end
  end
end

def get_metadata(key, default)
  ScraperWiki.get_var(key, default)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  retry
end

def save_metadata(key, value)
  ScraperWiki.save_var(key, value)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
  retry
end

BASE_URL = 'https://www.psi.gov.sg'
Mechanize.html_parser = Nokogiri::HTML

# 0-31 and 127 are control characters, 32 is space, '%' is considered an
# invalid character, '_' is considered a wildcard.
CHARS = [*33..126].map{|s|s.chr.downcase}.uniq - ['%', '_']

initial = {}
1.upto(MAX_KEY_LENGTH).each do |i|
  initial[i] = get_metadata(metadata_key(i), CHARS.first)
end

# "~_" returns fewer than 500 results, so no need to worry about 2nd+ letters.
if initial[1] == CHARS.last
  1.upto(MAX_KEY_LENGTH).each do |i|
    initial[i] = CHARS.first
    save_metadata(metadata_key(i), initial[i])
  end
end

puts "Initial prefix is #{initial.sort_by{|i,letter| i}.reduce(''){|memo,(i,letter)| memo + letter}.sub(/!+\Z/, '')}"

CHARS[CHARS.index(initial[1])..-1].each do |a|
  save_metadata(metadata_key(1), a)
  if !download(a + '_') # '_' is considered a wildcard
    CHARS[CHARS.index(initial[2])..-1].each do |b|
      save_metadata(metadata_key(2), b)
      download(a + b)
    end
    reset_metadata(2)
    initial[2] = CHARS.first
  end
end
