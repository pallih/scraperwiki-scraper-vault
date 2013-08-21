require 'nokogiri'

xml = ScraperWiki::scrape("http://184.72.174.87/MembersData/services/mnis/ReferenceData/AddressTypes/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//AddressType").each do |addresstype|
  data = {
      address_type_id: addresstype.xpath('AddressType_Id').text,
      name: addresstype.xpath('Name').text,
      is_physical_address: addresstype.xpath('IsPhysicalAddress').text
    }
    ScraperWiki::save_sqlite(['address_type_id'], data)
end
