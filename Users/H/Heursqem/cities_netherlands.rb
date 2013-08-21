# Blank Ruby

require 'open-uri'
require 'nokogiri'
require 'scraperwiki'
require 'csv'

def last_level (level, url, page_nr)
                   
   html_doc = Nokogiri::HTML(open("http://www.dmoz.org" + url))
   puts url 
   html_tables = html_doc.search("div[@class='dir-1 borN']")

   if html_tables.size > 0

     html_records = html_tables[0].search("ul[@class='directory dir-col']")
     # puts html_records

     number_of_records = html_records.search('li').count - 1
     # puts number_of_records + 1
   
     record_data = html_records.search('li')[0..number_of_records]
     record_data.each_with_index do |counter, x|

       href_attrib = counter.search('a')[0].get_attribute('href') 
       last_level_city = counter.search('a')[0].text

       # puts last_level_city

       if last_level_city == "Streken" or
          last_level_city == "Bedrijven en Economie" or
          last_level_city == "Gezondheid" or
          last_level_city == "Kunst en Amusement" or
          last_level_city == "Maatschappij" or
          last_level_city == "Onderwijs" or
          last_level_city == "Recreatie en Sport" 
         puts "skip, don't register the name"
       else

          if level == 1
             $data_level_1 = last_level_city
             $data_level_2 = ""
             $data_level_3 = ""
             $data_level_4 = ""
             $data_level_5 = ""
             $data_level_6 = ""
           end           

           if level == 2
             $data_level_2 = last_level_city
           end           
           if level == 3
             $data_level_3 = last_level_city
           end           
           if level == 4
             $data_level_4 = last_level_city
           end           
           if level == 5
             $data_level_5 = last_level_city
           end           
           if level == 6
             $data_level_6 = last_level_city
           end

           if level < $max_level 
              last_level(level+1, href_attrib, 1)
           else
              ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4, "Level 5"=>$data_level_5, "Level 6"=>$data_level_5})
           end                           


       end # last_level_city == "Streken" or

     end # record_data.each_with_index do |counter, x|

   else
      ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4, "Level 5"=>$data_level_5, "Level 6"=>$data_level_5})



   end  # html_tables.size > 0


end  # def last_level (level, url, page_nr)


 $max_level = 4

 $data_level_1 = ""
 $data_level_2 = ""
 $data_level_3 = ""
 $data_level_4 = ""
 $data_level_5 = ""
 $data_level_6 = ""


  start_pagina = 1
  aantal_levels = 6
  start_level = 1

  last_level(start_level, '/World/Nederlands/Regionaal/Nederland/', start_pagina)

  

