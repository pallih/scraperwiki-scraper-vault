# We use the Flickr API to construct a table
require 'nokogiri'

# STARTS HERE: define tag to look for 
tag=Array.[]("911")

for i in 0..2 do
  base_URI="http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=c03a81a10d6d8a8e3c3e3a9ee3767300&tags="+tag[i]+"&page="

  xml = ScraperWiki.scrape(base_URI)
  puts xml
  record = {}

  # Next we use Nokogiri to extract the values from the XML returned from the API
  doc = Nokogiri::HTML(xml)
  doc.search('photo').each do |photo|
      $URL= "http://www.flickr.com/photos/"+ photo['owner'] +"/"+ photo ['id']
      puts $URL
      #record['URL']=$URL
      $UserID=photo['owner']
      $PhotoID=photo ['id']
      $User_URI="http://api.flickr.com/services/rest/?method=flickr.people.getInfo&api_key=c03a81a10d6d8a8e3c3e3a9ee3767300&user_id="+$UserID
      xml_user = ScraperWiki.scrape($User_URI)
      puts xml_user
      doc_user = Nokogiri::HTML(xml_user)
      doc_user.search('person').each do |person|
         puts person['path_alias']
         $Path_alias=person['path_alias']
         #record['Path_alias']=person['path_alias']
      end
      doc_user.search('username').each do |username|
         puts username.content
         #record['Username']=username.content
      end
      doc_user.search('location').each do |location|
         puts location.content
         #record['location']=location.content
      end
      #record['tag']=tag[i]
      #record['Photo_URL']="http://www.flickr.com/photos/"+$Path_alias+"/"+$PhotoID+"/sizes/l/"
      $Photo_URL="http://www.flickr.com/photos/"+$Path_alias+"/"+$PhotoID+"/sizes/l/"
      
      xml_photo= ScraperWiki.scrape($Photo_URL)
      puts xml_photo
      doc_user = Nokogiri::HTML(xml_photo)
      doc_user.search('div[@id="allsizes-photo"] > img').each do |photo|
         puts photo['src']
         record['Photo']=photo['src']
      end
    
      ScraperWiki.save(['Photo'], record)
  end
end