# coding: utf-8
require 'open-uri'
require 'nokogiri'
require 'json'

BASE_URL   = 'http://www.parl.gc.ca/MembersOfParliament/'
SOURCE_URL = BASE_URL + 'MainMPsCompleteList.aspx?TimePeriod=Current&Language=E'

# @todo document preferred caucus names
CAUCUS_MAP = {
  'Green Party' => 'Green',
  'NDP' => 'New Democratic',
}

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

Nokogiri::HTML(open(SOURCE_URL)).css('#MasterPage_MasterPage_BodyContent_PageContent_Content_ListContent_ListContent_grdCompleteList tr:gt(1)').each do |tr|
  # Scrape the list page.
  last_name, first_name, honorific = tr.at_css('td:eq(1)').text.match(/\A([^,]+?), ([^(]+?)(?: \((.+)\))?\z/)[1..3].compact.map(&:strip)
  first_name.squeeze!(' ')
  last_name.squeeze!(' ')
  party_name = tr.at_css('td:eq(4)').text
  data = {
    'district_name'  => tr.at_css('td:eq(2)').text,
    'elected_office' => 'MP',
    'source_url'     => SOURCE_URL,
    'first_name'     => first_name,
    'last_name'      => last_name,
    'party_name'     => CAUCUS_MAP[party_name] || party_name,
    'url'            => BASE_URL + tr.at_css('td:eq(1) a')[:href],
    'extra'          => {},
  }
  data['extra']['honorific_prefix'] = honorific if honorific

  # Scrape the details page.
  key = data['url'][/Key=(\d+)/, 1]
  string = open("http://www.parl.gc.ca/MembersOfParliament/PrintProfileMP.aspx?Key=#{key}&Language=E").read
  doc = Nokogiri::HTML(string, nil, 'utf-8')
  src = doc.at_css('#MasterPage_TombstoneContent_TombstoneContent_ucHeaderMP_imgPhoto')[:src]

  data.merge!({
    'email' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_hlEMail').text,
    'photo_url' => "http://www.parl.gc.ca/MembersOfParliament/#{src}",
    'personal_url' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_hlWebSite').text,
    'offices' => [],
  })

  if doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_divHouseAddress')
    data['offices'] << {
      'type' => 'legislature',
      'postal' => [
        doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblHOCAddressLine1').text, # address
        doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblHOCAddressLine2').text, # city, region
        doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblHOCAddressLine3').text, # postal code
      ].join("\n"),
      'tel' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblTelephoneData').text.strip,
      'fax' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblFaxData').text.strip,
    }
  end

  if doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_divConstituencyOffices')
    doc.css('#MasterPage_DetailsContent_DetailsContent_ctl00_divConstituencyOffices table td').each_slice(8) do |slice|
      data['offices'] << {
        'type' => 'constituency',
        'postal' => [
          slice[0].text, # address
          slice[1].text, # city, region
          slice[2].text, # postal code
        ].join("\n"),
        'tel' => slice[4].text.sub('Telephone: ', '').strip,
        'fax' => slice[5].text.sub('Fax: ', '').strip,
      }
    end
  end

  data['extra']['preferred_language'] = doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblPrefLanguageData').text

  data['extra'] = data['extra'].to_json
  data['offices'] = data['offices'].to_json
  ScraperWiki.save_sqlite(['district_name'], data)
end# coding: utf-8
require 'open-uri'
require 'nokogiri'
require 'json'

BASE_URL   = 'http://www.parl.gc.ca/MembersOfParliament/'
SOURCE_URL = BASE_URL + 'MainMPsCompleteList.aspx?TimePeriod=Current&Language=E'

# @todo document preferred caucus names
CAUCUS_MAP = {
  'Green Party' => 'Green',
  'NDP' => 'New Democratic',
}

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

Nokogiri::HTML(open(SOURCE_URL)).css('#MasterPage_MasterPage_BodyContent_PageContent_Content_ListContent_ListContent_grdCompleteList tr:gt(1)').each do |tr|
  # Scrape the list page.
  last_name, first_name, honorific = tr.at_css('td:eq(1)').text.match(/\A([^,]+?), ([^(]+?)(?: \((.+)\))?\z/)[1..3].compact.map(&:strip)
  first_name.squeeze!(' ')
  last_name.squeeze!(' ')
  party_name = tr.at_css('td:eq(4)').text
  data = {
    'district_name'  => tr.at_css('td:eq(2)').text,
    'elected_office' => 'MP',
    'source_url'     => SOURCE_URL,
    'first_name'     => first_name,
    'last_name'      => last_name,
    'party_name'     => CAUCUS_MAP[party_name] || party_name,
    'url'            => BASE_URL + tr.at_css('td:eq(1) a')[:href],
    'extra'          => {},
  }
  data['extra']['honorific_prefix'] = honorific if honorific

  # Scrape the details page.
  key = data['url'][/Key=(\d+)/, 1]
  string = open("http://www.parl.gc.ca/MembersOfParliament/PrintProfileMP.aspx?Key=#{key}&Language=E").read
  doc = Nokogiri::HTML(string, nil, 'utf-8')
  src = doc.at_css('#MasterPage_TombstoneContent_TombstoneContent_ucHeaderMP_imgPhoto')[:src]

  data.merge!({
    'email' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_hlEMail').text,
    'photo_url' => "http://www.parl.gc.ca/MembersOfParliament/#{src}",
    'personal_url' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_hlWebSite').text,
    'offices' => [],
  })

  if doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_divHouseAddress')
    data['offices'] << {
      'type' => 'legislature',
      'postal' => [
        doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblHOCAddressLine1').text, # address
        doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblHOCAddressLine2').text, # city, region
        doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblHOCAddressLine3').text, # postal code
      ].join("\n"),
      'tel' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblTelephoneData').text.strip,
      'fax' => doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblFaxData').text.strip,
    }
  end

  if doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_divConstituencyOffices')
    doc.css('#MasterPage_DetailsContent_DetailsContent_ctl00_divConstituencyOffices table td').each_slice(8) do |slice|
      data['offices'] << {
        'type' => 'constituency',
        'postal' => [
          slice[0].text, # address
          slice[1].text, # city, region
          slice[2].text, # postal code
        ].join("\n"),
        'tel' => slice[4].text.sub('Telephone: ', '').strip,
        'fax' => slice[5].text.sub('Fax: ', '').strip,
      }
    end
  end

  data['extra']['preferred_language'] = doc.at_css('#MasterPage_DetailsContent_DetailsContent_ctl00_lblPrefLanguageData').text

  data['extra'] = data['extra'].to_json
  data['offices'] = data['offices'].to_json
  ScraperWiki.save_sqlite(['district_name'], data)
end