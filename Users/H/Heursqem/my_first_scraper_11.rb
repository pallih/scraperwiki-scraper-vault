require 'open-uri'
require 'nokogiri'
require 'scraperwiki'
require 'csv'

hospdoc = Nokogiri::HTML(open("http://www.geopostcodes.com/netherlands_zip_codes"))
tables = hospdoc.search("table[@id='browser']")

numofrecords = tables[0].search('tr').count - 2
recorddata = tables[0].search('tr')[1..numofrecords]

recorddata.each_with_index do |hosp, i|

 hrefattrib = hosp.search('td')[0].search('a')[0].get_attribute('href') 

 gemeente = hosp.search('td')[0].search('a')[0].text
 
 url_2 = "http://www.geopostcodes.com/"+ hrefattrib
 download_2 = open(url_2)
 doc_2  = Nokogiri::HTML(download_2)
 tables2 = doc_2.search("table[@id='browser']")
 numofrecords2 = tables2[0].search('tr').count - 1
 
 recorddata2 = tables2[0].search('tr')[1..numofrecords2]
 
 recorddata2.each_with_index do |hosp2, k|

    if k == numofrecords2 -1 
       hrefattrib2b = hosp2.search('td')[0].search('font')[0].search('a')[0] 
       puts hrefattrib2b
       if hrefattrib2b 
            robbie = hrefattrib2b.get_attribute('href')
            puts robbie
       

# hier komt de hele text nog een keer

             url_4 = "http://www.geopostcodes.com/"+ robbie
             download_4 = open(url_4)
             doc_4  = Nokogiri::HTML(download_4)
             tables4 = doc_4.search("table[@id='browser']")
             numofrecords4 = tables4[0].search('tr').count - 2
 
             recorddata4 = tables4[0].search('tr')[1..numofrecords4]
 
             recorddata4.each_with_index do |hosp4, z|
  
                 hrefattrib4 = hosp4.search('td')[0].search('a')[0].get_attribute('href') 
                 # puts hrefattrib4
  
                 gemeente4 = hosp4.search('td')[0].search('a')[0].text

                 if gemeente4 == 'Bonaire' or gemeente4 == 'Saba' or gemeente4 == 'Sint Eustatius'
                    puts 'Bonaire dus eigenlijk niets doen'
                 else 

                   url_5 = "http://www.geopostcodes.com/"+ hrefattrib4
                   download_5 = open(url_5)
                   doc_5  = Nokogiri::HTML(download_5)
                   tables5 = doc_5.search("table[@id='browser']")
                   numofrecords5 = tables5[0].search('tr').count - 2
 
                   recorddata5 = tables5[0].search('tr')[1..numofrecords5]
 
                   recorddata5.each_with_index do |hosp5, l|

                           hrefattrib5 = hosp5.search('td')[0].search('a')[0].get_attribute('href') 
                           # puts hrefattrib5
  
                           gemeente5 = hosp5.search('td')[0].search('a')[0].text
      
                           # puts gemeente + ' : ' + gemeente2 + ' : ' + gemeente3
     
                           ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3"], data={"Level 1"=>gemeente, "Level 2"=>gemeente4, "Level 3"=>gemeente5})


                   end
                end  



 
            end




# tot en met hier 
       else
            puts '2de level bestaat uit slechts 1 pagina'
       end


    else

         hrefattrib2 = hosp2.search('td')[0].search('a')[0].get_attribute('href') 
         # puts hrefattrib2
   
         gemeente2 = hosp2.search('td')[0].search('a')[0].text
         if gemeente2 == 'Bonaire' or gemeente2 == 'Saba' or gemeente2 == 'Sint Eustatius'
            puts 'Bonaire dus eigenlijk niets doen'
         else 
           url_3 = "http://www.geopostcodes.com/"+ hrefattrib2
           download_3 = open(url_3)
           doc_3  = Nokogiri::HTML(download_3)
           tables3 = doc_3.search("table[@id='browser']")
           numofrecords3 = tables3[0].search('tr').count - 2
     
           recorddata3 = tables3[0].search('tr')[1..numofrecords3]
     
           recorddata3.each_with_index do |hosp3, l|
      
              # hrefattrib3 = hosp3.search('td')[0].search('a')[0].get_attribute('href') 
              # puts hrefattrib3
        
              gemeente3 = hosp3.search('td')[0].search('a')[0].text
    
              # puts gemeente + ' : ' + gemeente2 + ' : ' + gemeente3
 
              ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3"], data={"Level 1"=>gemeente, "Level 2"=>gemeente2, "Level 3"=>gemeente3})
     
            end
         end
     end
  end
  
endrequire 'open-uri'
require 'nokogiri'
require 'scraperwiki'
require 'csv'

hospdoc = Nokogiri::HTML(open("http://www.geopostcodes.com/netherlands_zip_codes"))
tables = hospdoc.search("table[@id='browser']")

numofrecords = tables[0].search('tr').count - 2
recorddata = tables[0].search('tr')[1..numofrecords]

recorddata.each_with_index do |hosp, i|

 hrefattrib = hosp.search('td')[0].search('a')[0].get_attribute('href') 

 gemeente = hosp.search('td')[0].search('a')[0].text
 
 url_2 = "http://www.geopostcodes.com/"+ hrefattrib
 download_2 = open(url_2)
 doc_2  = Nokogiri::HTML(download_2)
 tables2 = doc_2.search("table[@id='browser']")
 numofrecords2 = tables2[0].search('tr').count - 1
 
 recorddata2 = tables2[0].search('tr')[1..numofrecords2]
 
 recorddata2.each_with_index do |hosp2, k|

    if k == numofrecords2 -1 
       hrefattrib2b = hosp2.search('td')[0].search('font')[0].search('a')[0] 
       puts hrefattrib2b
       if hrefattrib2b 
            robbie = hrefattrib2b.get_attribute('href')
            puts robbie
       

# hier komt de hele text nog een keer

             url_4 = "http://www.geopostcodes.com/"+ robbie
             download_4 = open(url_4)
             doc_4  = Nokogiri::HTML(download_4)
             tables4 = doc_4.search("table[@id='browser']")
             numofrecords4 = tables4[0].search('tr').count - 2
 
             recorddata4 = tables4[0].search('tr')[1..numofrecords4]
 
             recorddata4.each_with_index do |hosp4, z|
  
                 hrefattrib4 = hosp4.search('td')[0].search('a')[0].get_attribute('href') 
                 # puts hrefattrib4
  
                 gemeente4 = hosp4.search('td')[0].search('a')[0].text

                 if gemeente4 == 'Bonaire' or gemeente4 == 'Saba' or gemeente4 == 'Sint Eustatius'
                    puts 'Bonaire dus eigenlijk niets doen'
                 else 

                   url_5 = "http://www.geopostcodes.com/"+ hrefattrib4
                   download_5 = open(url_5)
                   doc_5  = Nokogiri::HTML(download_5)
                   tables5 = doc_5.search("table[@id='browser']")
                   numofrecords5 = tables5[0].search('tr').count - 2
 
                   recorddata5 = tables5[0].search('tr')[1..numofrecords5]
 
                   recorddata5.each_with_index do |hosp5, l|

                           hrefattrib5 = hosp5.search('td')[0].search('a')[0].get_attribute('href') 
                           # puts hrefattrib5
  
                           gemeente5 = hosp5.search('td')[0].search('a')[0].text
      
                           # puts gemeente + ' : ' + gemeente2 + ' : ' + gemeente3
     
                           ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3"], data={"Level 1"=>gemeente, "Level 2"=>gemeente4, "Level 3"=>gemeente5})


                   end
                end  



 
            end




# tot en met hier 
       else
            puts '2de level bestaat uit slechts 1 pagina'
       end


    else

         hrefattrib2 = hosp2.search('td')[0].search('a')[0].get_attribute('href') 
         # puts hrefattrib2
   
         gemeente2 = hosp2.search('td')[0].search('a')[0].text
         if gemeente2 == 'Bonaire' or gemeente2 == 'Saba' or gemeente2 == 'Sint Eustatius'
            puts 'Bonaire dus eigenlijk niets doen'
         else 
           url_3 = "http://www.geopostcodes.com/"+ hrefattrib2
           download_3 = open(url_3)
           doc_3  = Nokogiri::HTML(download_3)
           tables3 = doc_3.search("table[@id='browser']")
           numofrecords3 = tables3[0].search('tr').count - 2
     
           recorddata3 = tables3[0].search('tr')[1..numofrecords3]
     
           recorddata3.each_with_index do |hosp3, l|
      
              # hrefattrib3 = hosp3.search('td')[0].search('a')[0].get_attribute('href') 
              # puts hrefattrib3
        
              gemeente3 = hosp3.search('td')[0].search('a')[0].text
    
              # puts gemeente + ' : ' + gemeente2 + ' : ' + gemeente3
 
              ScraperWiki.save_sqlite(unique_keys=["Level 1", "Level 2", "Level 3"], data={"Level 1"=>gemeente, "Level 2"=>gemeente2, "Level 3"=>gemeente3})
     
            end
         end
     end
  end
  
end