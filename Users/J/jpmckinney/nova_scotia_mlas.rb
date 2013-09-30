require 'json'
require 'open-uri'
require 'spreadsheet'

SOURCE_URL = 'http://nslegislature.ca/pdfs/people/addresses/mlaconstadd.xls'

CAUCUS_MAP = {
  'I'   => 'Independent',
  'L'   => 'Liberal',
  'NDP' => 'New Democratic',
  'PC'  => 'Progressive Conservative',
}

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

Spreadsheet.open(open(SOURCE_URL)).worksheet(0).each_with_index do |row,index|
  # Skip header row
  next if index == 0
  # Party name is part of name column
  prefix, name, party_name = row[1].match(/\A(Honourable)? ?([^(]+) \(([^)]+)\)/)[1..3]
  data = {
    'name'           => name.strip,
    'district_name'  => row[0],
    'elected_office' => 'MLA',
    'source_url'     => SOURCE_URL,
    'party_name'     => CAUCUS_MAP[party_name],
    'email'          => row[4],
    'offices'        => [
      {
        'type'     => 'constituency',
        'postal'   => row[5].sub(', Nova Scotia', ' NS'),
      },
    ],
  }
  data.merge!({'extra' => {
    'honorific_prefix' => prefix.sub('Honourable', 'Hon.'),
  }.to_json}) if prefix
  unless row[3].nil? or row[3].empty? 
    data['offices'][0]['fax'] = "#{row[3]}"
    unless data['offices'][0]['fax'][/\A\D*902/]
      data['offices'][0]['fax'] = "(902) #{data['offices'][0]['fax']}"
    end
  end
  # Handle multiple phone numbers per field
  tels = row[2].split(' or ').map{|tel| tel.gsub(/\D/, '')}.each do |tel|
    key = data['offices'][0].key?('tel') ? 'alt' : 'tel'
    case tel.size
    when 7
      data['offices'][0][key] = "#{tel.sub(/(\d{3})(\d{4})/, '\1-\2')}"
      unless data['offices'][0][key][/\A\D*902/]
        data['offices'][0][key] = "(902) #{data['offices'][0][key]}"
      end
    when 11
      data['offices'][0]['tollfree'] = tel.sub(/(\d)(\d{3})(\d{3})(\d{4})/, '\1-\2-\3-\4')
    else
      data['offices'][0][key] = tel
    end
  end
  data['offices'] = data['offices'].to_json
  ScraperWiki.save_sqlite(['district_name'], data)
endrequire 'json'
require 'open-uri'
require 'spreadsheet'

SOURCE_URL = 'http://nslegislature.ca/pdfs/people/addresses/mlaconstadd.xls'

CAUCUS_MAP = {
  'I'   => 'Independent',
  'L'   => 'Liberal',
  'NDP' => 'New Democratic',
  'PC'  => 'Progressive Conservative',
}

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

Spreadsheet.open(open(SOURCE_URL)).worksheet(0).each_with_index do |row,index|
  # Skip header row
  next if index == 0
  # Party name is part of name column
  prefix, name, party_name = row[1].match(/\A(Honourable)? ?([^(]+) \(([^)]+)\)/)[1..3]
  data = {
    'name'           => name.strip,
    'district_name'  => row[0],
    'elected_office' => 'MLA',
    'source_url'     => SOURCE_URL,
    'party_name'     => CAUCUS_MAP[party_name],
    'email'          => row[4],
    'offices'        => [
      {
        'type'     => 'constituency',
        'postal'   => row[5].sub(', Nova Scotia', ' NS'),
      },
    ],
  }
  data.merge!({'extra' => {
    'honorific_prefix' => prefix.sub('Honourable', 'Hon.'),
  }.to_json}) if prefix
  unless row[3].nil? or row[3].empty? 
    data['offices'][0]['fax'] = "#{row[3]}"
    unless data['offices'][0]['fax'][/\A\D*902/]
      data['offices'][0]['fax'] = "(902) #{data['offices'][0]['fax']}"
    end
  end
  # Handle multiple phone numbers per field
  tels = row[2].split(' or ').map{|tel| tel.gsub(/\D/, '')}.each do |tel|
    key = data['offices'][0].key?('tel') ? 'alt' : 'tel'
    case tel.size
    when 7
      data['offices'][0][key] = "#{tel.sub(/(\d{3})(\d{4})/, '\1-\2')}"
      unless data['offices'][0][key][/\A\D*902/]
        data['offices'][0][key] = "(902) #{data['offices'][0][key]}"
      end
    when 11
      data['offices'][0]['tollfree'] = tel.sub(/(\d)(\d{3})(\d{3})(\d{4})/, '\1-\2-\3-\4')
    else
      data['offices'][0][key] = tel
    end
  end
  data['offices'] = data['offices'].to_json
  ScraperWiki.save_sqlite(['district_name'], data)
end