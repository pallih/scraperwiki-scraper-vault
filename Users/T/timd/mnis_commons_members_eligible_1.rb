require 'nokogiri'

xml = ScraperWiki::scrape("http://184.72.174.87/MembersData/services/mnis/members/query/House=Commons%7CIsEligible=true/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//Member").each do |member|
  data = {
      member_id: member.xpath('@Member_Id').text,
      dods_id: member.xpath('@Dods_Id').text,
      pims_id: member.xpath('@Pims_Id').text,

      display_as: member.xpath('DisplayAs').text,
      list_as: member.xpath('ListAs').text,
      full_title: member.xpath('FullTitle').text,
      date_of_birth: member.xpath('DateOfBirth').text,
      date_of_death: member.xpath('DateOfDeath').text,
      gender: member.xpath('Gender').text,
      party: member.xpath('Party').text,
      party_id: member.xpath('Party/@Id').text,
      house: member.xpath('House').text,
      member_from: member.xpath('MemberFrom').text,
      house_start_date: member.xpath('HouseStartDate').text,
      house_end_date: member.xpath('HouseEndDate').text,
      current_status_id: member.xpath('CurrentStatus/@Id').text,
      current_status_is_active: member.xpath('CurrentStatus/@IsActive').text,
      current_status_name: member.xpath('CurrentStatus/Name').text,
      current_status_reason: member.xpath('CurrentStatus/Reason').text,
      current_status_start_date: member.xpath('CurrentStatus/StartDate').text,


    }
    ScraperWiki::save_sqlite(['member_id'], data)
end

require 'nokogiri'

xml = ScraperWiki::scrape("http://184.72.174.87/MembersData/services/mnis/members/query/House=Commons%7CIsEligible=true/")
       
@doc = Nokogiri::XML(xml)

@doc.xpath("//Member").each do |member|
  data = {
      member_id: member.xpath('@Member_Id').text,
      dods_id: member.xpath('@Dods_Id').text,
      pims_id: member.xpath('@Pims_Id').text,

      display_as: member.xpath('DisplayAs').text,
      list_as: member.xpath('ListAs').text,
      full_title: member.xpath('FullTitle').text,
      date_of_birth: member.xpath('DateOfBirth').text,
      date_of_death: member.xpath('DateOfDeath').text,
      gender: member.xpath('Gender').text,
      party: member.xpath('Party').text,
      party_id: member.xpath('Party/@Id').text,
      house: member.xpath('House').text,
      member_from: member.xpath('MemberFrom').text,
      house_start_date: member.xpath('HouseStartDate').text,
      house_end_date: member.xpath('HouseEndDate').text,
      current_status_id: member.xpath('CurrentStatus/@Id').text,
      current_status_is_active: member.xpath('CurrentStatus/@IsActive').text,
      current_status_name: member.xpath('CurrentStatus/Name').text,
      current_status_reason: member.xpath('CurrentStatus/Reason').text,
      current_status_start_date: member.xpath('CurrentStatus/StartDate').text,


    }
    ScraperWiki::save_sqlite(['member_id'], data)
end

