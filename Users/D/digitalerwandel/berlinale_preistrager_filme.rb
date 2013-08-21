require 'nokogiri'

i = 970

#ALLE 579 TABELLENSEITEN EINLESEN
for page in 2011..2012
  
  #EINZELNE TABELLESEITE EINLESEN
  html = ScraperWiki::scrape("http://www.berlinale.de/de/archiv/jahresarchive/#{page}/03_preistrger_#{page}/03_preistraeger_#{page}.html")
  doc = Nokogiri::XML(html)   

  counter = 0

    #LAND
    doc.css('table.prizeWinners tbody tr td.col2').each do |row|
          preis_film = row.content
          puts i, preis_film, page
          ScraperWiki::save_sqlite([:ID], data={'ID'=>i, 'Jahr' => page, 'Preis_Film'=>preis_film}, table_name='Berlinale-Preistraeger_Film')
          i = i + 1
    end

    sleep 30
end