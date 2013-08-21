require 'open-uri'
require 'nokogiri'

BASE_URL   = 'http://www.parl.gc.ca/MembersOfParliament/'
SOURCE_URL = BASE_URL + 'MainMPsCompleteList.aspx?TimePeriod=Current&Language=E'

CAUCUS_MAP = {
  'Green Party' => 'Green',
  'NDP' => 'New Democratic',
}

Nokogiri::HTML(open(SOURCE_URL)).css('#MasterPage_MasterPage_BodyContent_PageContent_Content_ListContent_ListContent_grdCompleteList tr:gt(1)').each do |tr|
  last_name, first_name = tr.at_css('td:eq(1)').text.match(/\A([^,]+), ([^(]+)/)[1..2].map(&:strip)#
  source = BASE_URL + tr.at_css('td:eq(2)').at_css('a')[:href]

  party_name = tr.at_css('td:eq(4)').text
  data = {
    'name'           => [first_name, last_name].join(' '),
    'district_name'  => tr.at_css('td:eq(2)').text,
    'elected_office' => 'MP',
    'source_url'     => source,
    'first_name'     => first_name,
    'last_name'      => last_name,
    'party_name'     => CAUCUS_MAP[party_name] || party_name,
    'url'            => BASE_URL + tr.at_css('td:eq(1) a')[:href],
  }
  ScraperWiki.save_sqlite(['district_name'], data)
  break
end

def scrapeExtended (data)
  
end