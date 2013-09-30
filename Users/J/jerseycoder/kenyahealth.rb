# Blank Ruby
require 'pdf-reader'
require 'open-uri'
require 'csv'
require 'net/http'

############ PDF STUFF - IGNORE IF NOT DOING PDF
#reader = PDF::Reader.new(io)

#puts reader.pdf_version
#puts reader.info
#puts reader.metadata
#puts reader.page_count

#text = reader.pages[18]
#puts page.fonts
#lines=text.split('\n')
############# END OF PDF STUFF

http = Net::HTTP.new("opendata.go.ke", 443)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE
# Get the poverty data
http.start do |http|
   req = Net::HTTP::Get.new("/api/views/i5bp-z9aq/rows.csv?accessType=DOWNLOAD")
   response = http.request(req)
   resp = response.body
   CSV.parse(resp).each do |row|
      unless row[0] == 'District Name'
     ScraperWiki.save_sqlite(unique_keys=['district name', 'poverty rate'], data={"district name" => row[0], "poverty rate" => row[1]} , table_name="Poverty")
    end # end unless first row
  end
end
# Who Diagnosed
http.start do |http|
   req = Net::HTTP::Get.new("/api/views/tfam-4f43/rows.csv?accessType=DOWNLOAD")
   response = http.request(req)
   resp = response.body
   CSV.parse(resp).each do |row|
     unless row[0] == 'District Name'
     ScraperWiki.save_sqlite(unique_keys=['district name', 'med worker at hospital', 'med worker at other health facility', 'traditional healer', 'non household member', 'household member', 'self', 'herbalist', 'faith healer', 'others'], data={"district name" => row[0], "med worker at hospital" => row[1], "med worker at other health facility" => row[2], "traditional healer" => row[3], "non household member" => row[4], "household member" => row[5], "self" => row[6], "herbalist" => row[7], "faith healer" => row[8], "others" => row[9] } , table_name="Who_Diagnosed")
    end # end unless first row
  end
end
# Join the tables
ScraperWiki.attach("kenyahealth")
joined2 = ScraperWiki.sqliteexecute("SELECT 'Poverty'.'district name', 'Poverty'.'poverty rate', 'Who_Diagnosed'.'med worker at hospital', 'Who_Diagnosed'.'med worker at other health facility', 'Who_Diagnosed'.'traditional healer', 'Who_Diagnosed'.'non household member',  'Who_Diagnosed'.'household member', 'Who_Diagnosed'.'self', 'Who_Diagnosed'.'herbalist', 'Who_Diagnosed'.'faith healer', 'Who_Diagnosed'.'others' from 'Poverty','Who_Diagnosed' WHERE 'Poverty'.'district name' = 'Who_Diagnosed'.'district name'")

# save the joined data table into a scraperwiki table, format floats, get rid of percent signs
joined2['data'].each do |d|   
   ScraperWiki.save_sqlite(unique_keys=['District Name', 'Poverty Rate', 'Med worker at hospital', 'Med worker at other health facility', 'Traditional healer', 'Non household member', 'Household member',  'Self', 'Herbalist', 'Faith healer', 'Others'], data={'District Name' => d[0], 'Poverty Rate' => (d[1].chop)[0..4].to_f, 'Med worker at hospital' => (d[2].chop)[0..4].to_f, 'Med worker at other health facility' => (d[3].chop)[0..4].to_f, 'Traditional healer' => (d[4].chop)[0..4].to_f, 'Non household member' => (d[5].chop)[0..4].to_f, 'Household member' => (d[6].chop)[0..4].to_f, 'Self' => (d[7].chop)[0..4].to_f, 'Herbalist' => (d[8].chop)[0..4].to_f, 'Faith healer' => (d[9].chop)[0..4].to_f,  'Others' => (d[10].chop)[0..4].to_f} , table_name="KenyaHealthbyDistrict")
end




# Blank Ruby
require 'pdf-reader'
require 'open-uri'
require 'csv'
require 'net/http'

############ PDF STUFF - IGNORE IF NOT DOING PDF
#reader = PDF::Reader.new(io)

#puts reader.pdf_version
#puts reader.info
#puts reader.metadata
#puts reader.page_count

#text = reader.pages[18]
#puts page.fonts
#lines=text.split('\n')
############# END OF PDF STUFF

http = Net::HTTP.new("opendata.go.ke", 443)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE
# Get the poverty data
http.start do |http|
   req = Net::HTTP::Get.new("/api/views/i5bp-z9aq/rows.csv?accessType=DOWNLOAD")
   response = http.request(req)
   resp = response.body
   CSV.parse(resp).each do |row|
      unless row[0] == 'District Name'
     ScraperWiki.save_sqlite(unique_keys=['district name', 'poverty rate'], data={"district name" => row[0], "poverty rate" => row[1]} , table_name="Poverty")
    end # end unless first row
  end
end
# Who Diagnosed
http.start do |http|
   req = Net::HTTP::Get.new("/api/views/tfam-4f43/rows.csv?accessType=DOWNLOAD")
   response = http.request(req)
   resp = response.body
   CSV.parse(resp).each do |row|
     unless row[0] == 'District Name'
     ScraperWiki.save_sqlite(unique_keys=['district name', 'med worker at hospital', 'med worker at other health facility', 'traditional healer', 'non household member', 'household member', 'self', 'herbalist', 'faith healer', 'others'], data={"district name" => row[0], "med worker at hospital" => row[1], "med worker at other health facility" => row[2], "traditional healer" => row[3], "non household member" => row[4], "household member" => row[5], "self" => row[6], "herbalist" => row[7], "faith healer" => row[8], "others" => row[9] } , table_name="Who_Diagnosed")
    end # end unless first row
  end
end
# Join the tables
ScraperWiki.attach("kenyahealth")
joined2 = ScraperWiki.sqliteexecute("SELECT 'Poverty'.'district name', 'Poverty'.'poverty rate', 'Who_Diagnosed'.'med worker at hospital', 'Who_Diagnosed'.'med worker at other health facility', 'Who_Diagnosed'.'traditional healer', 'Who_Diagnosed'.'non household member',  'Who_Diagnosed'.'household member', 'Who_Diagnosed'.'self', 'Who_Diagnosed'.'herbalist', 'Who_Diagnosed'.'faith healer', 'Who_Diagnosed'.'others' from 'Poverty','Who_Diagnosed' WHERE 'Poverty'.'district name' = 'Who_Diagnosed'.'district name'")

# save the joined data table into a scraperwiki table, format floats, get rid of percent signs
joined2['data'].each do |d|   
   ScraperWiki.save_sqlite(unique_keys=['District Name', 'Poverty Rate', 'Med worker at hospital', 'Med worker at other health facility', 'Traditional healer', 'Non household member', 'Household member',  'Self', 'Herbalist', 'Faith healer', 'Others'], data={'District Name' => d[0], 'Poverty Rate' => (d[1].chop)[0..4].to_f, 'Med worker at hospital' => (d[2].chop)[0..4].to_f, 'Med worker at other health facility' => (d[3].chop)[0..4].to_f, 'Traditional healer' => (d[4].chop)[0..4].to_f, 'Non household member' => (d[5].chop)[0..4].to_f, 'Household member' => (d[6].chop)[0..4].to_f, 'Self' => (d[7].chop)[0..4].to_f, 'Herbalist' => (d[8].chop)[0..4].to_f, 'Faith healer' => (d[9].chop)[0..4].to_f,  'Others' => (d[10].chop)[0..4].to_f} , table_name="KenyaHealthbyDistrict")
end




