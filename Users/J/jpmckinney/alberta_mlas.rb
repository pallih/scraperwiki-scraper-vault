require 'mechanize'
require 'csv'
require 'json'

SOURCE_URL = 'http://www.assembly.ab.ca/net/index.aspx?p=mla_csv'

# http://www.assembly.ab.ca/net/index.aspx?p=mla_home
CAUCUS_MAP = {
  'AB' => 'Alberta',
  'AL' => 'Liberal',
  'ND' => 'New Democratic',
  'PC' => 'Progressive Conservative',
  'W'  => 'Wildrose',
}

OFFICE_TYPE_MAP = {
  'Legislature Office' => 'legislature',
  'Constituency Office' => 'constituency',
}

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DROP TABLE swdata'
end

# Download the CSV
agent = Mechanize.new
page = agent.get SOURCE_URL
{ '_ctl0:radlstGroup' => 'Information for All MLAs',
  '_ctl0:chklstFields:0' => 'on',
  '_ctl0:chklstFields:1' => 'on',
  '_ctl0:chklstFields:2' => 'on',
  '_ctl0:btnCreateCSV' => "Create '.csv' file",
}.each do |field,value|
  page.form[field] = value
end
page = page.form.submit
file = page.link_with(:href => /tempcsv/).click

# Ignore fields: MLA Title, MLA Middle Names, Country
CSV.parse(file.body, :headers => true).each do |row|
  # Last name sometimes has the postnominal "QC" for "Queen's Counsel"
  last_name = row['MLA Last Name'].sub(', QC', '')

  offices = [{
    'type'     => OFFICE_TYPE_MAP[row[8]],
    'postal'   => [row[9], row[10], row[11], row[12], row[14]].reject(&:empty?).join("\n"),
    'tel'      => row[15],
    'fax'      => row[16],
  }]

  extra = {
    'honorific_prefix' => row['MLA Title']
  }
  unless row[18][/pending/i]
    offices << {
      'type'     => OFFICE_TYPE_MAP[row[17]],
      'postal'   => [row[18], row[19], row[20], row[21], row[23]].reject(&:empty?).join("\n"),
      'tel'      => row[24],
      'tollfree' => row[25],
      'fax'      => row[26],
    }

  end
  
  data = {
    'district_name'  => row['Riding Name'],
    'elected_office' => 'MLA',
    'source_url'     => SOURCE_URL,
    'first_name'     => row['MLA First Name'],
    'last_name'      => last_name,
    'party_name'     => CAUCUS_MAP[row['Caucus']],
    'email'          => row['MLA Email'].empty? ? row['Email'] : row['MLA Email'],
    'district_id'    => row['Riding Number'],
    # There are two of each of the address columns
    'offices'        => offices.to_json,
    'extra'          => extra.to_json
  }
  ScraperWiki.save_sqlite(['district_id'], data)
end
