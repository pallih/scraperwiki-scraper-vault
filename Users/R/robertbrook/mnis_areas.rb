require 'nokogiri'

xml = ScraperWiki::scrape("http://184.72.174.87/MembersData/services/mnis/ReferenceData/Areas/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//Area").each do |area|
  data = {
      area_id: area.xpath('Area_Id').text,
      name: area.xpath('Name').text,
      notes: area.xpath('Notes').text,
      ons_area_id: area.xpath('OnsAreaId').text,
      area_type: area.xpath('AreaType').text,
      area_type_id: area.xpath('AreaType_Id').text,
    }
    ScraperWiki::save_sqlite(['area_id'], data)
end
require 'nokogiri'

xml = ScraperWiki::scrape("http://184.72.174.87/MembersData/services/mnis/ReferenceData/Areas/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//Area").each do |area|
  data = {
      area_id: area.xpath('Area_Id').text,
      name: area.xpath('Name').text,
      notes: area.xpath('Notes').text,
      ons_area_id: area.xpath('OnsAreaId').text,
      area_type: area.xpath('AreaType').text,
      area_type_id: area.xpath('AreaType_Id').text,
    }
    ScraperWiki::save_sqlite(['area_id'], data)
end
