# coding: utf-8

# CivicInfo BC gets support from Ministry of Community, Sport and Cultural Development.
# http://www.civicinfo.bc.ca/70.asp#3

# Will not provide digital copy of database.
# http://www.civicinfo.bc.ca/50.asp#3

require 'csv'
require 'json'
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www.civicinfo.bc.ca/'

puts 'Get Census subdivision populations'
POPULATIONS = {}
# Remove the first line of the CSV.
CSV.parse(open('http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=301&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-301.CSV').read.sub(/\A.+\n/, ''), headers: true).each do |row|
  break if row.empty? # Extra content after table
  POPULATIONS[row['Geographic code'].to_s] = row['Population, 2011'].to_i
end

puts 'Get Census subdivisions'
CENSUS_SUBDIVISIONS = JSON.parse(open('http://public.slashpoundbang.com/csds.json').read)

# Map municipality types to Census subdivision types.
#
# @see http://www12.statcan.gc.ca/census-recensement/2006/ref/symb-ab-acr-eng.cfm#cst
TYPE_MAP = {
  'City'                         => 'CY',
  'District'                     => 'DM',
  'Indian Government District'   => 'IGD',
  'Island Municipality'          => 'IM',
  'Islands Trust'                => 'IST', # Designated place
  'Mountain Resort Municipality' => 'VL',
  'Regional District'            => 'RD', # Census division
  'Regional Municipality'        => 'RGM',
  'Resort Municipality'          => 'DM',
  'Town'                         => 'T',
  'Township'                     => 'DM',
  'Village'                      => 'VL',
}

# Map municipality names to Census subdivision names.
NAME_MAP = {
  '100 Mile House' => 'One Hundred Mile House',
  'Sun Peaks' => 'Sun Peaks Mountain',
}

def match_census_subdivision(name, type = nil)
  district_id = nil

  name = NAME_MAP[name] || name
  type = TYPE_MAP[type] || type
  matches = CENSUS_SUBDIVISIONS.select do |_,x|
    x['name'] == name && x['type'] == type && x['province'] == 'British Columbia / Colombie-Britannique'
  end

  case matches.size
  when 1
    district_id = matches.keys.first
  when 0
    puts "No Census subdivision found with name '#{name}', type '#{type}'"
  else
    puts "Multiple Census subdivisions found with '#{name}', type '#{type}'"
  end

  district_id
end

# Skip municipalities for which we have scrapers.
SKIP = [
  'Vancouver',
  'Victoria',
  #'Surrey',
  #'Burnaby',
  #'Richmond',
  #'Abbotsford',
  #'Coquitlam',
]

def scrape(url)
  url = BASE_URL + url
  doc = Nokogiri::HTML open(url)

  municipality = doc.at_css('font[size="4"] b').text
  type = doc.at_css('font[size="4"] i').text

  a = doc.at_xpath('//a[text()="Next"]')
  continue = lambda{ scrape(a[:href]) if a }

  if type == 'Regional District'
    # @todo treat the 27 Regional Districts differently
    continue.call
    return
  elsif doc.at_xpath('//font[text()="Electoral Area or Municipality"]')
    puts "Census division? #{url}"
    continue.call
    return
  end

  csduid = match_census_subdivision municipality, type
  # #match_census_subdivision will warn if +csduid+ is nil.
  if csduid.nil? or SKIP.include?(municipality)
    continue.call
    return
  end

  shared = {
    district_name: municipality,
    district_id: csduid,
  }

  shared_postal = []
  shared_office = {}
  last_key = nil
  doc.css('table[border="0"]:not([cellpadding]) tr').each do |tr|
    next if ['facebook.com', 'linkedin.com', 'twitter.com', 'youtube.com', 'YouTube.com'].find{|x| tr.at_css(%(a[href*="#{x}"]))}
    key = tr.at_css('td:eq(1)').text.gsub(/[[:space:]]+/, ' ')
    value = tr.at_css('td:eq(2)').text.strip

    case key
    when 'Incorporated', 'Regional District'
      # Do nothing
    when 'Mailing Address', 'Street Address'
      shared_postal << value
    when 'Phone'
      shared_office[:tel] = value
    when 'Fax'
      shared_office[:fax] = value
    when 'URL'
      shared[:url] = value
    when 'General email'
      shared[:email] = value
    when ''
      if last_key == 'Street Address'
        shared_postal << value
      else
        puts "Empty key after '#{last_key}' on #{url}"
      end
    else
      puts "Unknown key '#{key}' on #{url}"
    end
    last_key = key unless key.empty? 
  end

  shared_office[:postal] = shared_postal.join "\n"

  doc.at_css('.thinborders_borderbottom').css('tr:not([bgcolor])').each do |tr|
    name_a = tr.at_css('td:eq(1) a')
    data = shared.merge({
      name: name_a.text.gsub(/[[:space:]]+/, ' '),
      elected_office: tr.at_css('td:eq(2)').text,
      url: BASE_URL + name_a[:href],
      source_url: url.sub(/&r.+\z/, ''),
    })
    page = Nokogiri::HTML(open(data[:url]))

    office = shared_office.dup
    last_key = nil
    page.css('table[cellpadding="3"] tr').each do |tr|
      next if tr.at_css('td:eq(2)').nil? 

      key = tr.at_css('td:eq(1)').text.gsub(/[[:space:]]+/, ' ').strip
      value = tr.at_css('td:eq(2)').text.strip

      case key
      when data[:name], 'Secondary Job Title'
        # Do nothing
      when 'Position', 'Primary Job Title'
        # Officials sometimes have multiple primary roles.
        unless [data[:elected_office], 'Electoral Area Director', 'Vice-Chair'].include?(value)
          puts "'#{value}' doesn't match '#{data[:elected_office]}' on #{data[:url]}"
        end
      when 'Phone'
        office[:tel] = value
      when 'Fax'
        office[:fax] = value
      when 'Toll Free Phone'
        office[:tollfree] = value
      when 'Email address', 'Primary Email'
        data[:email] = value unless value == 'n/a'
      when 'Secondary Email'
        data[:email] ||= value
      when ''
        if last_key.nil? 
          # Do nothing
        else
          puts "Empty key after '#{last_key}' on #{data[:url]}"
        end
      else
        puts "Unknown key '#{key}' on #{data[:url]}"
      end
      last_key = key unless key.empty? 
    end

    data[:offices] = [office].to_json
    ScraperWiki.save_sqlite(['url'], data)
  end

  # Go to next record.
  continue.call
end

puts 'Calculate population'
population = ScraperWiki.sqliteexecute('SELECT DISTINCT(district_id) FROM swdata')['data'].flatten.reduce(0) do |sum,csduid|
  puts "No population figure for Census subdivision #{csduid}" unless POPULATIONS.key? csduid
  sum + POPULATIONS[csduid].to_i
end
ScraperWiki.save_var('population', population)

puts 'Scrape mayors and councillors'
scrape Nokogiri::HTML(open(BASE_URL + '111.asp?showall=yes')).at_xpath('//a[text()="Details"]')[:href]

#def scrape_list(url)
#  doc = Nokogiri::HTML(open(BASE_URL + url))
#
#  doc.css('p').each do |p|
#    name = p.at_css('a').text
#    type = p.at_css('i').text
#    next if type == 'Regional District'
#    match_census_subdivision name, type
#  end
#
#  # Go to next page.
#  a = doc.at_xpath('//a[text()="next"]')
#  scrape_list(a[:href] + '&showall=yes') if a
#end
#
#scrape_list '111.asp?showall=yes'
