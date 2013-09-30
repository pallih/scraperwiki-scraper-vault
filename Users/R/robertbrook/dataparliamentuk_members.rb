require 'nokogiri'

xml = ScraperWiki::scrape("http://data.parliament.uk/resources/members/api/members.svc/commons/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//m:commonsMember").each do |member|
      print member.inspect

  data = {
      id: member.xpath('@m:id').text,
      dods_id: member.xpath('@m:dodsId').text,

      website: member.xpath('@m:website').text,

      title: member.xpath('m:title').text,
      party_id: member.xpath('p:party/@id').text,
      party_name: member.xpath('p:party/p:partyName').text,
      party_abbrev: member.xpath('p:party/p:partyAbbrev').text,
      party_sub_type: member.xpath('p:party/p:subType').text,
      constituency_id: member.xpath('c:constituency/@id').text,
      constituency_name: member.xpath('c:constituency/c:constituencyName').text,
      constituency_type: member.xpath('c:constituency/c:constituencyType').text,
      constituency_country: member.xpath('c:constituency/c:country').text,
      constituency_area_type: member.xpath('c:constituency/c:areaType').text,

      first_name: member.xpath('m:firstName').text,
      last_name: member.xpath('m:lastName').text,
      gender: member.xpath('g:gender').text,
      gender_id: member.xpath('g:gender/@id').text,

    }
    ScraperWiki::save_sqlite(['id'], data)
end
require 'nokogiri'

xml = ScraperWiki::scrape("http://data.parliament.uk/resources/members/api/members.svc/commons/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//m:commonsMember").each do |member|
      print member.inspect

  data = {
      id: member.xpath('@m:id').text,
      dods_id: member.xpath('@m:dodsId').text,

      website: member.xpath('@m:website').text,

      title: member.xpath('m:title').text,
      party_id: member.xpath('p:party/@id').text,
      party_name: member.xpath('p:party/p:partyName').text,
      party_abbrev: member.xpath('p:party/p:partyAbbrev').text,
      party_sub_type: member.xpath('p:party/p:subType').text,
      constituency_id: member.xpath('c:constituency/@id').text,
      constituency_name: member.xpath('c:constituency/c:constituencyName').text,
      constituency_type: member.xpath('c:constituency/c:constituencyType').text,
      constituency_country: member.xpath('c:constituency/c:country').text,
      constituency_area_type: member.xpath('c:constituency/c:areaType').text,

      first_name: member.xpath('m:firstName').text,
      last_name: member.xpath('m:lastName').text,
      gender: member.xpath('g:gender').text,
      gender_id: member.xpath('g:gender/@id').text,

    }
    ScraperWiki::save_sqlite(['id'], data)
end
