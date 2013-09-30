require 'nokogiri'  

# page: AHCityRep.asp

#forms: RPTYPE = p_OffSale, q_CityLOV = OAKLAND

html = ScraperWiki.scrape("http://www.abc.ca.gov/datport/AHCityRep.asp", {"RPTYPE" => "p_OffSale", "q_CityLOV" => "OAKLAND"})    
 
 
doc = Nokogiri::HTML(html)
for v in doc.search("tr.report_column")
  cells= v.search('td')
  if cells.length > 0
    data = {
      'LicenseNumber' => cells[1].inner_text ,
      'Status' => cells[2].inner_text ,
      'LicenseType' => cells[3].inner_text ,
      'OrigIssDate' => cells[4].inner_text ,
      'ExpirDate' => cells[5].inner_text ,
      'PremisesAddr' => cells[6].inner_text ,
      'BusinessName' => cells[7].inner_text ,
      'MailingAddress' => cells[8].inner_text ,
      'GeoCode'=> cells[9].inner_text 
    }
      ScraperWiki.save_sqlite(unique_keys=['LicenseNumber'], data=data) 
  end

end
require 'nokogiri'  

# page: AHCityRep.asp

#forms: RPTYPE = p_OffSale, q_CityLOV = OAKLAND

html = ScraperWiki.scrape("http://www.abc.ca.gov/datport/AHCityRep.asp", {"RPTYPE" => "p_OffSale", "q_CityLOV" => "OAKLAND"})    
 
 
doc = Nokogiri::HTML(html)
for v in doc.search("tr.report_column")
  cells= v.search('td')
  if cells.length > 0
    data = {
      'LicenseNumber' => cells[1].inner_text ,
      'Status' => cells[2].inner_text ,
      'LicenseType' => cells[3].inner_text ,
      'OrigIssDate' => cells[4].inner_text ,
      'ExpirDate' => cells[5].inner_text ,
      'PremisesAddr' => cells[6].inner_text ,
      'BusinessName' => cells[7].inner_text ,
      'MailingAddress' => cells[8].inner_text ,
      'GeoCode'=> cells[9].inner_text 
    }
      ScraperWiki.save_sqlite(unique_keys=['LicenseNumber'], data=data) 
  end

end
