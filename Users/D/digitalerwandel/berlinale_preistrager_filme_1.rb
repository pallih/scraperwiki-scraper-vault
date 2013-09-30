require 'nokogiri'

i = 1

#ALLE 76 TABELLENSEITEN EINLESEN
for page in 0..2 #75
  
  #EINZELNE TABELLENSEITE EINLESEN
  html = ScraperWiki::scrape("http://www.profoto.com/buy?page=#{page}")
  doc = Nokogiri::HTML.parse(html)  

  doc.xpath("//a[starts-with(@href, \"mailto:\")]/@href").each do |row|
  
    puts row.content
  
  end  

          #ScraperWiki::save_sqlite([:ID], data={'ID'=>i, 'E-Mail' => email}, table_name='Profoto E-Mail Adressen')
          i = i + 1
    #end

  puts i  
  sleep 5
endrequire 'nokogiri'

i = 1

#ALLE 76 TABELLENSEITEN EINLESEN
for page in 0..2 #75
  
  #EINZELNE TABELLENSEITE EINLESEN
  html = ScraperWiki::scrape("http://www.profoto.com/buy?page=#{page}")
  doc = Nokogiri::HTML.parse(html)  

  doc.xpath("//a[starts-with(@href, \"mailto:\")]/@href").each do |row|
  
    puts row.content
  
  end  

          #ScraperWiki::save_sqlite([:ID], data={'ID'=>i, 'E-Mail' => email}, table_name='Profoto E-Mail Adressen')
          i = i + 1
    #end

  puts i  
  sleep 5
end