# coding: utf-8

require 'csv'
require 'json'
require 'open-uri'
require 'spreadsheet'

SOURCE_URL = 'http://municipalaffairs.alberta.ca/cfml/officials/CEO_Council.xls'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

puts 'Get Census subdivision populations'
populations = {}
# Remove the first line of the CSV.
CSV.parse(open('http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=301&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-301.CSV').read.sub(/\A.+\n/, ''), headers: true).each do |row|
  break if row.empty? # Extra content after table
  populations[row['Geographic code'].to_s] = row['Population, 2011'].to_i
end

puts 'Get Census subdivisions'
CENSUS_SUBDIVISIONS = JSON.parse(open('http://public.slashpoundbang.com/csds.json').read)

# Map municipality types to Census subdivision types.
#
# Census subdivisions (First Nations): IRI, S-É
#
# @see http://www12.statcan.gc.ca/census-recensement/2006/ref/symb-ab-acr-eng.cfm#cst
TYPE_MAP = {
  'City'                     => 'CY',
  'Improvement District'     => 'ID',
  'Municipal District'       => 'MD',
  'Special Area'             => 'SA',
  'Specialized Municipality' => 'SM',
  'Summer Village'           => 'SV',
  'Town'                     => 'T',
  'Village'                  => 'VL',
}

# Map municipality names to Census subdivision names.
# CEO_Council.xls uses "Special Areas Board" for all three Special Areas.
NAME_MAP = {
  'Clear Hills County'                     => 'Clear Hills',
  'Kananaskis Improvement District'        => 'Kananaskis',
  'Newell County'                          => 'Newell County No. 4', # Statistics Canada outdated (2011)

  # Formatting.
  'Improvement District No. 04 (Waterton)' => 'Improvement District No.  4 Waterton',
  'Improvement District No. 09 (Banff)'    => 'Improvement District No.  9 Banff',
  'Lac La Biche County'                    => 'Lac la Biche County',
  'Lesser Slave River No. 124'             => 'Lesser Slave River No.124',
  'Lloydminster'                           => 'Lloydminster (Part)',
}

def match_census_subdivision(name, type = nil)
  district_id = nil

  name = NAME_MAP[name] || name
  type = TYPE_MAP[type] || type
  matches = CENSUS_SUBDIVISIONS.select do |_,x|
    x['name'] == name && x['type'] == type && x['province'] == 'Alberta'
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

puts 'Match Alberta municipalities with districts'
# Some CY and SM have districts. All MD have districts.
# http://www.municipalaffairs.alberta.ca/am_types_of_municipalities_in_alberta.cfm
csds_with_districts = [
  # List any municipalities for which we have customs scrapers:
  ['Grande Prairie', 'CY'],

  # CY
  ['Calgary', 'CY'],
  ['Edmonton', 'CY'],
  # Airdrie
  # Brooks
  # Camrose
  # Cold Lake
  # Fort Saskatchewan
  # Grande Prairie
  # Lacombe
  # Leduc
  # Lethbridge
  # Lloydminster (Part)
  # Medicine Hat
  # Red Deer
  # Spruce Grove
  # St. Albert
  # Wetaskiwin

  # SM
  ['Mackenzie County', 'SM'],
  ['Strathcona County', 'SM'],
  ['Wood Buffalo', 'SM'],
  # Jasper
  # Crowsnest Pass

  # MD
  ['Acadia No. 34', 'MD'],
  ['Athabasca County', 'MD'],
  ['Barrhead County No. 11', 'MD'],
  ['Beaver County', 'MD'],
  ['Big Lakes', 'MD'],
  ['Bighorn No. 8', 'MD'],
  ['Birch Hills County', 'MD'],
  ['Bonnyville No. 87', 'MD'],
  ['Brazeau County', 'MD'],
  ['Camrose County', 'MD'],
  ['Cardston County', 'MD'],
  ['Clear Hills', 'MD'],
  ['Clearwater County', 'MD'],
  ['Cypress County', 'MD'],
  ['Fairview No. 136', 'MD'],
  ['Flagstaff County', 'MD'],
  ['Foothills No. 31', 'MD'],
  ['Forty Mile County No. 8', 'MD'],
  ['Grande Prairie County No. 1', 'MD'],
  ['Greenview No. 16', 'MD'],
  ['Kneehill County', 'MD'],
  ['Lac la Biche County', 'MD'],
  ['Lac Ste. Anne County', 'MD'],
  ['Lacombe County', 'MD'],
  ['Lamont County', 'MD'],
  ['Leduc County', 'MD'],
  ['Lesser Slave River No.124', 'MD'],
  ['Lethbridge County', 'MD'],
  ['Minburn County No. 27', 'MD'],
  ['Mountain View County', 'MD'],
  ['Newell County No. 4', 'MD'],
  ['Northern Lights County', 'MD'],
  ['Northern Sunrise County', 'MD'],
  ['Opportunity No. 17', 'MD'],
  ['Paintearth County No. 18', 'MD'],
  ['Parkland County', 'MD'],
  ['Peace No. 135', 'MD'],
  ['Pincher Creek No. 9', 'MD'],
  ['Ponoka County', 'MD'],
  ['Provost No. 52', 'MD'],
  ['Ranchland No. 66', 'MD'],
  ['Red Deer County', 'MD'],
  ['Rocky View County', 'MD'],
  ['Saddle Hills County', 'MD'],
  ['Smoky Lake County', 'MD'],
  ['Smoky River No. 130', 'MD'],
  ['Spirit River No. 133', 'MD'],
  ['St. Paul County No. 19', 'MD'],
  ['Starland County', 'MD'],
  ['Stettler County No. 6', 'MD'],
  ['Sturgeon County', 'MD'],
  ['Taber', 'MD'],
  ['Thorhild County No. 7', 'MD'],
  ['Two Hills County No. 21', 'MD'],
  ['Vermilion River County', 'MD'],
  ['Vulcan County', 'MD'],
  ['Wainwright No. 61', 'MD'],
  ['Warner County No. 5', 'MD'],
  ['Westlock County', 'MD'],
  ['Wetaskiwin County No. 10', 'MD'],
  ['Wheatland County', 'MD'],
  ['Willow Creek No. 26', 'MD'],
  ['Woodlands County', 'MD'],
  ['Yellowhead County', 'MD'],
].map{|name, type|
  match_census_subdivision name, type
}.compact

GENDER_MAP = {
  'Mr.' => 'M',
  'Ms.' => 'F',
}

puts 'Calculate population'
population = ScraperWiki.sqliteexecute('SELECT DISTINCT(district_id) FROM swdata')['data'].flatten.reduce(0) do |sum,csduid|
  puts "No population figure for Census subdivision #{csduid}" unless populations.key? csduid
  sum + populations[csduid].to_i
end
ScraperWiki.save_var('population', population)

puts 'Scrape mayors and councillors'
Spreadsheet.open(open(SOURCE_URL)).worksheet(0).each_with_index do |row,index|
  # Skip header row.
  next if index == 0

  # Remove common prefixes and reorder "County".
  name = row[3].sub(/\A(City|Municipal District|Municipality|Regional Municipality|Summer Village|Town|Village) of /, '')
  name.sub!(/\ACounty of (.+?)( No\. \d+)?\z/, '\1 County\2')

  csduid = match_census_subdivision name, row[1]
  # #match_census_subdivision will warn if +csduid+ is nil.
  next if csduid.nil? or csds_with_districts.include?(csduid)

  unless row[7].nil? && row[8] == 'Vacant'
    elected_office = if row[4].nil? && row[7] == 'Colin' && row[8] == 'Adair'
      'Councillor'
    else
      row[4] && row[4].gsub(/\A[[:space:]]+|[[:space:]]+\z/, '')
    end

    if elected_office.nil? 
      puts "No elected office for #{row[7]} #{row[8]} in #{name}"
    else
      gender = GENDER_MAP[row[6]]
      puts "Couldn't determine gender: '#{row[6]}'" if gender.nil? 
      ScraperWiki.save_sqlite(['index'], {
        index: index,
        elected_office: elected_office,
        first_name: row[7].gsub(/\A[[:space:]]+|[[:space:]]+\z/, '').squeeze(' '),
        last_name: row[8].gsub(/\A[[:space:]]+|[[:space:]]+\z/, '').squeeze(' '),
        offices: [{
          postal: row[9..10].compact.join("\n") + "\n#{row[11]} #{row[13]}  #{row[12]}",
          tel: row[15],
          fax: row[16],
        }].to_json,
        email: row[17] == '-' ? nil : row[17],
        url: row[18] && "http://#{row[18]}",
        gender: gender,
        district_id: csduid,
        district_name: NAME_MAP[name] || name,
        source_url: SOURCE_URL,
      })
    end
  end
end

