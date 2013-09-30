require 'open-uri'
require 'nokogiri'
require 'scraperwiki'
require 'csv'

def last_level (level, url, page_nr)
                   
                   html_doc = Nokogiri::HTML(open("http://www.geopostcodes.com/"+ url))
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
                             # href_attrib = counter.search('td')[0].search('a')[0].get_attribute('href') 

                             dummy_1 = counter.search('td')[0]
                             if dummy_1 
                                dummy_2 = dummy_1.search('a')[0]
                                if dummy_2 
                                   last_level_city = dummy_2.text
                                

                                   # last_level_city = counter.search('td')[0].search('a')[0].text
                                   puts last_level_city

                                  if level == 3
                                     $data_level_3 = last_level_city
                                  end           
                                  if level == 4
                                     $data_level_4 = last_level_city
                                  end     

                                  # puts 'last_level_city =' + last_level_city
                                  #schrijf data


                                  ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end


                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end


                          end
                   end
                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end


end

def normal_level (level, max_level, url, page_nr)
                   
                   html_doc = Nokogiri::HTML(open("http://www.geopostcodes.com/"+ url))
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
                                normal_level(level, max_level, href_another_page, volgende_pagina)
                             end           
                          else
                             href_attrib = counter.search('td')[0].search('a')[0].get_attribute('href') 
                             last_level_city = counter.search('td')[0].search('a')[0].text

                             if level == 1
                                $data_level_1 = last_level_city
                                $data_level_2 = ""
                                $data_level_3 = ""
                                $data_level_4 = ""
                             end           
                             if level == 2
                                $data_level_2 = last_level_city
                             end           
                             if level == 3
                                $data_level_3 = last_level_city
                             end     
      
    

                             if level == max_level - 1
                               if last_level_city == "Bonaire" or last_level_city == "Saba" or last_level_city == "Sint Eustatius" 
                                  puts "Bonaire"
                                  ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                               else
                                  last_level(level+1, href_attrib, 1)
                               end 
                             else
                               normal_level(level+1, max_level, href_attrib, 1)
                             end
                          end
                   end

                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end




end


 $data_level_1 = ""
 $data_level_2 = ""
 $data_level_3 = ""
 $data_level_4 = ""


  start_pagina = 1
  aantal_levels = 4
  start_level = 1

  # last_level(start_level, 'index.php?pg=browse&grp=1&sort=1&niv=5&id=137531&l=0', start_pagina)

  normal_level(start_level, aantal_levels, 'germany_zip_codes', start_pagina)
  

require 'open-uri'
require 'nokogiri'
require 'scraperwiki'
require 'csv'

def last_level (level, url, page_nr)
                   
                   html_doc = Nokogiri::HTML(open("http://www.geopostcodes.com/"+ url))
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
                             # href_attrib = counter.search('td')[0].search('a')[0].get_attribute('href') 

                             dummy_1 = counter.search('td')[0]
                             if dummy_1 
                                dummy_2 = dummy_1.search('a')[0]
                                if dummy_2 
                                   last_level_city = dummy_2.text
                                

                                   # last_level_city = counter.search('td')[0].search('a')[0].text
                                   puts last_level_city

                                  if level == 3
                                     $data_level_3 = last_level_city
                                  end           
                                  if level == 4
                                     $data_level_4 = last_level_city
                                  end     

                                  # puts 'last_level_city =' + last_level_city
                                  #schrijf data


                                  ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end


                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end


                          end
                   end
                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end


end

def normal_level (level, max_level, url, page_nr)
                   
                   html_doc = Nokogiri::HTML(open("http://www.geopostcodes.com/"+ url))
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
                                normal_level(level, max_level, href_another_page, volgende_pagina)
                             end           
                          else
                             href_attrib = counter.search('td')[0].search('a')[0].get_attribute('href') 
                             last_level_city = counter.search('td')[0].search('a')[0].text

                             if level == 1
                                $data_level_1 = last_level_city
                                $data_level_2 = ""
                                $data_level_3 = ""
                                $data_level_4 = ""
                             end           
                             if level == 2
                                $data_level_2 = last_level_city
                             end           
                             if level == 3
                                $data_level_3 = last_level_city
                             end     
      
    

                             if level == max_level - 1
                               if last_level_city == "Bonaire" or last_level_city == "Saba" or last_level_city == "Sint Eustatius" 
                                  puts "Bonaire"
                                  ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                               else
                                  last_level(level+1, href_attrib, 1)
                               end 
                             else
                               normal_level(level+1, max_level, href_attrib, 1)
                             end
                          end
                   end

                else 
                         ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3", "Level 4"], data={"Level 1"=>$data_level_1, "Level 2"=>$data_level_2, "Level 3"=>$data_level_3, "Level 4"=>$data_level_4})
                end




end


 $data_level_1 = ""
 $data_level_2 = ""
 $data_level_3 = ""
 $data_level_4 = ""


  start_pagina = 1
  aantal_levels = 4
  start_level = 1

  # last_level(start_level, 'index.php?pg=browse&grp=1&sort=1&niv=5&id=137531&l=0', start_pagina)

  normal_level(start_level, aantal_levels, 'germany_zip_codes', start_pagina)
  

