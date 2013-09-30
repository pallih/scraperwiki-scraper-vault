# Blank Ruby

require 'open-uri'
require 'nokogiri'
require 'scraperwiki'
require 'csv'

def schrijf_regel
   if $data_level_1 == $data_vorig_1  and
      $data_level_2 == $data_vorig_2  and
      $data_level_3 == $data_vorig_3  and
      $data_level_4 == $data_vorig_4  and
      $data_level_5 == $data_vorig_5  and
      $data_level_6 == $data_vorig_6  
    then
       #alles hetzelfde dus niets doen
    else
       ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4, "Level 5"=>$data_level_5, "Level 6"=>$data_level_5})
       $aantal_records = $aantal_records + 1
     end
  $data_vorig_1 = $data_level_1
  $data_vorig_2 = $data_level_2
  $data_vorig_3 = $data_level_3
  $data_vorig_4 = $data_level_4
  $data_vorig_5 = $data_level_5
  $data_vorig_6 = $data_level_6
end


def last_level (level, url, page_nr)
   html_doc = Nokogiri::HTML(open("http://www.geopostcodes.com/" + url))
   html_tables = html_doc.search("table[@id='browser']")

   if html_tables.size > 0

     number_of_records = html_tables[0].search('tr').count - 1
   
     record_data = html_tables[0].search('tr')[1..number_of_records]
     record_data.each_with_index do |counter, x|

        if x == (number_of_records - 1) 
           another_page = counter.search('td')[0].search('font')[0].search('a')[page_nr - 1]
           if another_page
              href_another_page = another_page.get_attribute('href')
              volgende_pagina = page_nr + 1
              last_level(level, href_another_page, volgende_pagina)
            end           
         else
 
            href_attrib = counter.search('a')[0].get_attribute('href') 
            last_level_city = counter.search('a')[0].text

            if last_level_city == 'Freiburg' or
               last_level_city == "Bayern" or
               last_level_city == "Karlsruhe" or
               last_level_city == "Stuttgart" or
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
                   if last_level_city == ''
                      schrijf_regel
                   else 
                      last_level(level+1, href_attrib, 1)
                   end
                else
                   schrijf_regel
                end                           


            end # last_level_city == "Streken" or

        end # x == (number_of_records - 1) 

     end # record_data.each_with_index do |counter, x|

   else
     schrijf_regel


   end  # html_tables.size > 0


end  # def last_level (level, url, page_nr)


 $max_level = 4

 $data_level_1 = ""
 $data_level_2 = ""
 $data_level_3 = ""
 $data_level_4 = ""
 $data_level_5 = ""
 $data_level_6 = ""

 $aantal_records = 0

 $data_vorig_1 = ""
 $data_vorig_2 = ""
 $data_vorig_3 = ""
 $data_vorig_4 = ""
 $data_vorig_5 = ""
 $data_vorig_6 = ""



  start_pagina = 1
  aantal_levels = 6
  start_level = 1

  last_level(start_level, '/index.php?pg=browse&grp=1&sort=1&niv=3&id=460&l=0', start_pagina)

  


# Blank Ruby

require 'open-uri'
require 'nokogiri'
require 'scraperwiki'
require 'csv'

def schrijf_regel
   if $data_level_1 == $data_vorig_1  and
      $data_level_2 == $data_vorig_2  and
      $data_level_3 == $data_vorig_3  and
      $data_level_4 == $data_vorig_4  and
      $data_level_5 == $data_vorig_5  and
      $data_level_6 == $data_vorig_6  
    then
       #alles hetzelfde dus niets doen
    else
       ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4, "Level 5"=>$data_level_5, "Level 6"=>$data_level_5})
       $aantal_records = $aantal_records + 1
     end
  $data_vorig_1 = $data_level_1
  $data_vorig_2 = $data_level_2
  $data_vorig_3 = $data_level_3
  $data_vorig_4 = $data_level_4
  $data_vorig_5 = $data_level_5
  $data_vorig_6 = $data_level_6
end


def last_level (level, url, page_nr)
   html_doc = Nokogiri::HTML(open("http://www.geopostcodes.com/" + url))
   html_tables = html_doc.search("table[@id='browser']")

   if html_tables.size > 0

     number_of_records = html_tables[0].search('tr').count - 1
   
     record_data = html_tables[0].search('tr')[1..number_of_records]
     record_data.each_with_index do |counter, x|

        if x == (number_of_records - 1) 
           another_page = counter.search('td')[0].search('font')[0].search('a')[page_nr - 1]
           if another_page
              href_another_page = another_page.get_attribute('href')
              volgende_pagina = page_nr + 1
              last_level(level, href_another_page, volgende_pagina)
            end           
         else
 
            href_attrib = counter.search('a')[0].get_attribute('href') 
            last_level_city = counter.search('a')[0].text

            if last_level_city == 'Freiburg' or
               last_level_city == "Bayern" or
               last_level_city == "Karlsruhe" or
               last_level_city == "Stuttgart" or
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
                   if last_level_city == ''
                      schrijf_regel
                   else 
                      last_level(level+1, href_attrib, 1)
                   end
                else
                   schrijf_regel
                end                           


            end # last_level_city == "Streken" or

        end # x == (number_of_records - 1) 

     end # record_data.each_with_index do |counter, x|

   else
     schrijf_regel


   end  # html_tables.size > 0


end  # def last_level (level, url, page_nr)


 $max_level = 4

 $data_level_1 = ""
 $data_level_2 = ""
 $data_level_3 = ""
 $data_level_4 = ""
 $data_level_5 = ""
 $data_level_6 = ""

 $aantal_records = 0

 $data_vorig_1 = ""
 $data_vorig_2 = ""
 $data_vorig_3 = ""
 $data_vorig_4 = ""
 $data_vorig_5 = ""
 $data_vorig_6 = ""



  start_pagina = 1
  aantal_levels = 6
  start_level = 1

  last_level(start_level, '/index.php?pg=browse&grp=1&sort=1&niv=3&id=460&l=0', start_pagina)

  


