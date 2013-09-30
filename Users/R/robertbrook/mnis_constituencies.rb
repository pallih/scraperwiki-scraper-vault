require 'nokogiri'

xml = ScraperWiki::scrape("http://184.72.174.87/MembersData/services/mnis/ReferenceData/Constituencies/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//Constituency").each do |constituency|
  data = {
      constituency_id: constituency.xpath('Constituency_Id').text,
      name: constituency.xpath('Name').text,
      alpha_name: constituency.xpath('AlphaName').text,
      constituency_type: constituency.xpath('ConstituencyType').text,
      constituency_type_id: constituency.xpath('ConstituencyType_Id').text,
      locata_id: constituency.xpath('LocataId').text,
      prev_constituency_id: constituency.xpath('PrevConstituencyId').text,

      old_dods_id: constituency.xpath('OldDodsId').text,
      old_dis_id: constituency.xpath('OldDisId').text,
      clerks_constituency_id: constituency.xpath('ClerksConstituencyId').text,
      clerks_constituency_name: constituency.xpath('ClerksConstituencyName').text,
      gid_id: constituency.xpath('GisId').text,
      pca_code: constituency.xpath('PcaCode').text,
      pcon_name: constituency.xpath('PconName').text,
      os_name: constituency.xpath('OsName').text,
      start_date: constituency.xpath('StartDate').text,
      end_date: constituency.xpath('EndDate').text,
      created_from_constituency: constituency.xpath('CreatedFromConstituency').text,
      created_from_constituency_id: constituency.xpath('CreatedFromConstituency_Id').text

    }
    ScraperWiki::save_sqlite(['constituency_id'], data)
end
require 'nokogiri'

xml = ScraperWiki::scrape("http://184.72.174.87/MembersData/services/mnis/ReferenceData/Constituencies/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//Constituency").each do |constituency|
  data = {
      constituency_id: constituency.xpath('Constituency_Id').text,
      name: constituency.xpath('Name').text,
      alpha_name: constituency.xpath('AlphaName').text,
      constituency_type: constituency.xpath('ConstituencyType').text,
      constituency_type_id: constituency.xpath('ConstituencyType_Id').text,
      locata_id: constituency.xpath('LocataId').text,
      prev_constituency_id: constituency.xpath('PrevConstituencyId').text,

      old_dods_id: constituency.xpath('OldDodsId').text,
      old_dis_id: constituency.xpath('OldDisId').text,
      clerks_constituency_id: constituency.xpath('ClerksConstituencyId').text,
      clerks_constituency_name: constituency.xpath('ClerksConstituencyName').text,
      gid_id: constituency.xpath('GisId').text,
      pca_code: constituency.xpath('PcaCode').text,
      pcon_name: constituency.xpath('PconName').text,
      os_name: constituency.xpath('OsName').text,
      start_date: constituency.xpath('StartDate').text,
      end_date: constituency.xpath('EndDate').text,
      created_from_constituency: constituency.xpath('CreatedFromConstituency').text,
      created_from_constituency_id: constituency.xpath('CreatedFromConstituency_Id').text

    }
    ScraperWiki::save_sqlite(['constituency_id'], data)
end
