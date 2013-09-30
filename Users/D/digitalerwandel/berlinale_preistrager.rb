require 'nokogiri'

i = 970

#ALLE 579 TABELLENSEITEN EINLESEN
for page in 2011..2012
  
  #EINZELNE TABELLESEITE EINLESEN
  html = ScraperWiki::scrape("http://www.berlinale.de/de/archiv/jahresarchive/#{page}/03_preistrger_#{page}/03_preistraeger_#{page}.html")
  doc = Nokogiri::XML(html)   

  counter = 0

    #LAND
    doc.css('table.prizeWinners tbody tr td.col1').each do |row|
          preis = row.content
          puts i, preis, page
          ScraperWiki::save_sqlite([:ID], data={'ID'=>i, 'Jahr' => page, 'Preis'=>preis}, table_name='Berlinale-Preistraeger')
          i = i + 1
    end

    sleep 10
endrequire 'nokogiri'

i = 970

#ALLE 579 TABELLENSEITEN EINLESEN
for page in 2011..2012
  
  #EINZELNE TABELLESEITE EINLESEN
  html = ScraperWiki::scrape("http://www.berlinale.de/de/archiv/jahresarchive/#{page}/03_preistrger_#{page}/03_preistraeger_#{page}.html")
  doc = Nokogiri::XML(html)   

  counter = 0

    #LAND
    doc.css('table.prizeWinners tbody tr td.col1').each do |row|
          preis = row.content
          puts i, preis, page
          ScraperWiki::save_sqlite([:ID], data={'ID'=>i, 'Jahr' => page, 'Preis'=>preis}, table_name='Berlinale-Preistraeger')
          i = i + 1
    end

    sleep 10
end