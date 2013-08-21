require 'nokogiri'

i = 11260

#ALLE 579 TABELLENSEITEN EINLESEN
for page in 564..579 #579
  
  #EINZELNE TABELLESEITE EINLESEN
  html = ScraperWiki::scrape("http://www.berlinale.de/de/archiv/archivsuche/Archivsuche.php?rp=1&page=#{page}&searchareas=programm&lang=DE")
  doc = Nokogiri::XML(html)    

  counter = 0
  for row in 1..20
    data = {
      ID: i = i + 1,
      Titel: doc.css('table tr td.col1 a.filmtitel')[counter].inner_text,
      Jahr: doc.css('table tr td.year')[counter].inner_text,
      Sektion: doc.css('table tr td.col2')[counter].inner_text
    }
   
     counter = counter + 1
     puts data
     ScraperWiki::save_sqlite([:ID], data, table_name='Berlinale-Filme')
    
   end
    
    #LAND
    #doc.css('table tr td.col1 br').each do |row|
        #if row.content[1] != ":"
          #land = row.content
          #i = i + 1
          #puts i, land
          #ScraperWiki::save_sqlite(unique_keys=["ID"], data={'ID'=>i, 'Land'=>land}, table_name='Berlinale-Filme')
        #end
    #end


    sleep 25
end